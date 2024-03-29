﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.SqlClient;

namespace WindowsFormsApp1
{
	public partial class Form1 : Form
	{
		Color restColor = Color.WhiteSmoke, hoverColor = Color.DarkGray, filledColor = Color.Black;
		int buttonSize = 20, padding = 2, gridOffsetX = 100, gridOffsetY = 30;
		int pieceButtonSize = 30, pieceButtonPadding = 10, pieceOffsetX = 50, pieceOffsetY = 30, pieceButtonSeparation = 220;
		Button[,] grid = new Button[7, 7];
		bool[,] gridFlags = new bool[7, 7];
		Button[,] pieces = new Button[2, 4];
		bool[,] pieceFlags = new bool[2, 4];
		int[] score = new int[2];
		int turn = 0;
		bool pieceBeingPlaced = false;
		PieceButton currentPiece = new PieceButton(-1, -1);
		TextBox score1, score2;
		public Form1()
		{
			InitializeComponent();
			for(int i = 0; i < 7; i++) {
				for (int j = 0; j < 7; j++) {
					Button b = new GridButton(i,j);
					this.Controls.Add(b);
					b.SetBounds(
						(i * (buttonSize + padding)) + gridOffsetX, 
						(j * (buttonSize + padding)) + gridOffsetY, 
						buttonSize, 
						buttonSize);
					b.BackColor = restColor;
					b.Click += new EventHandler(this.grid_clicked);
					b.MouseMove += new MouseEventHandler(this.grid_hover);
					b.MouseLeave += new EventHandler(this.grid_hover_end);
					grid[i, j] = b;
				}
			}
			for (int i = 0; i < 2; i++) {
				for (int j = 0; j < 4; j++) {
					PieceButton b = new PieceButton(j, i);
					this.Controls.Add(b);
					pieces[i, j] = b;
					b.SetBounds(
						(pieceOffsetX + (i*pieceButtonSeparation)),
						(j * (pieceButtonSize + pieceButtonPadding)) + pieceOffsetY,
						pieceButtonSize,
						pieceButtonSize);
					b.Click += new EventHandler(this.player_option_clicked);
				}
			}
			this.score1 = new TextBox();
			this.Controls.Add(score1);
			score1.SetBounds(400, 100, 50, 50);
			score1.Text = this.score[0].ToString();
			this.score2 = new TextBox();
			this.Controls.Add(score2);
			score2.SetBounds(450, 100, 50, 50);
			score2.Text = this.score[1].ToString();
		}

		private void Form1_Load(object sender, EventArgs e){

		}
		private void place_piece_by_action(int action) {
			if (action > 196) throw new Exception("action is out of bounds");
			int x = (action % 49)/7, y = (action % 49) % 7;
			int piece = action / 49;
			this.pieces[turn, piece].PerformClick();
			this.grid[x, y].PerformClick();
		}
		private void grid_clicked(object sender, EventArgs e){
			GridButton btn = (GridButton)sender;
			if (pieceBeingPlaced && is_possible_piece(currentPiece.pieceID, btn.x, btn.y)) {
				btn.BackColor = filledColor;
				this.grid[btn.x + pieceLegs(currentPiece.pieceID)[0], btn.y].BackColor = filledColor;
				this.grid[btn.x, btn.y + pieceLegs(currentPiece.pieceID)[1]].BackColor = filledColor;
				this.gridFlags[btn.x, btn.y] = true;
				this.gridFlags[btn.x + pieceLegs(currentPiece.pieceID)[0], btn.y] = true;
				this.gridFlags[btn.x, btn.y + pieceLegs(currentPiece.pieceID)[1]] = true;
				pieceBeingPlaced = false;
				this.pieceFlags[currentPiece.playerID, currentPiece.pieceID] = true;
				currentPiece.BackColor = hoverColor;
				reset_pieces(currentPiece.playerID);
				update_score();
				this.turn = (this.turn * -1) + 1;
				reset_board();
			}
		}
		private void reset_board() {
			for (int i = 0; i < 4; i++){
				if (!pieceFlags[turn, i]){
					for (int j = 0; j < 7; j++) {
						for (int k = 0; k < 7; k++) {
							if (is_possible_piece(i, j, k)) return;
						}
					}
				}
			}
			for (int i = 0; i < 7; i++) {
				for (int j = 0; j < 7; j++) {
					gridFlags[i, j] = false;
					grid[i, j].BackColor = restColor;
				}
			}
		}
		private void update_score(){
			bool[] rows = new bool[7], columns = new bool[7];
			this.score[0] += 7;
			this.score[1] += 7;
			for (int i = 0; i < 7; i++) {
				for (int j = 0; j < 7; j++){
					if (!this.gridFlags[i, j]) {
						if (!rows[i]) {
							rows[i] = true;
							this.score[0]--;
						}
						if (!columns[j]){
							columns[j] = true;
							this.score[1]--;
						}
					}
				}
			}
			for (int i = 0; i < 7; i++) {
				for (int j = 0; j < 7; j++) {
					if (!rows[i] || !columns[j]){
						this.gridFlags[i, j] = false;
						this.grid[i, j].BackColor = restColor;
					}
				}
			}
			this.score1.Text = this.score[0].ToString();
			this.score2.Text = this.score[1].ToString();
		}
		private void grid_hover(object sender, EventArgs e) {
			GridButton btn = (GridButton)sender;
			if (pieceBeingPlaced && is_possible_piece(currentPiece.pieceID, btn.x, btn.y)) {
				btn.BackColor = hoverColor;
				this.grid[btn.x + pieceLegs(currentPiece.pieceID)[0], btn.y].BackColor = hoverColor;
				this.grid[btn.x, btn.y + pieceLegs(currentPiece.pieceID)[1]].BackColor = hoverColor;
			}
		}
		private void grid_hover_end(object sender, EventArgs e) {
			if (pieceBeingPlaced) {
				foreach (GridButton btn in this.grid) {
					if (btn.BackColor == hoverColor) {
						btn.BackColor = restColor;
					}
				}
			}
		}
		private void player_option_clicked(object sender, EventArgs e){
			PieceButton btn = (PieceButton)sender;
			if(btn.playerID == turn && !pieceFlags[btn.playerID, btn.pieceID])
			{
				pieceBeingPlaced = true;
				currentPiece = btn;
			}
		}
		private void reset_pieces(int player) {
			for (int i = 0; i < 4; i++){
				if (!this.pieceFlags[player, i]) {
					return;
				}
			}
			for (int i = 0; i < 4; i++){
				this.pieceFlags[player, i] = false;
				this.pieces[player, i].BackColor = restColor;
			}
		}
		/* PIECE CONFIG
		 * 
		 * ID 0:
		 *  ##
		 *  #
		 * ID 1:
		 *  ##
		 *   #
		 * ID 2:
		 *  #
		 *  ##
		 * ID 3:
		 *   #
		 *  ##
		 */
		private int[] pieceLegs (int pieceID){
			int[] a = new int[2];
			switch (pieceID)
			{
				case 0:
					a[0] = 1;
					a[1] = 1;
					break;
				case 1:
					a[0] = -1;
					a[1] = 1;
					break;
				case 2:
					a[0] = 1;
					a[1] = -1;
					break;
				case 3:
					a[0] = -1;
					a[1] = -1;
					break;
				default:
					throw new Exception("piece ID out of bounds");
			}
			return a;
		}
		private bool is_possible_piece(int piece, int x, int y) {
			int[] a = new int[2], b= new int[2], c = new int[2];
			a[0] = x;
			a[1] = y;
			b[0] = x + pieceLegs(piece)[0];
			b[1] = y;
			c[0] = x;
			c[1] = y + pieceLegs(piece)[1];
			return (
				a[0] < 7 && a[0] >= 0 &&
				a[1] < 7 && a[1] >= 0 &&
				b[0] < 7 && b[0] >= 0 &&
				b[1] < 7 && b[1] >= 0 &&
				c[0] < 7 && c[0] >= 0 &&
				c[1] < 7 && c[1] >= 0 &&
				!this.gridFlags[a[0], a[1]] &&
				!this.gridFlags[b[0], b[1]] &&
				!this.gridFlags[c[0], c[1]]);
		}
	}
	public class PieceButton : Button {
		public int pieceID, playerID;
		public PieceButton(int piece, int player) {
			this.Text = piece.ToString();
			pieceID = piece;
			playerID = player;
		}
	}
	public class GridButton : Button {
		public int x, y;
		public GridButton(int coordX, int coordY) {
			x = coordX;
			y = coordY;
		}
	}
}
