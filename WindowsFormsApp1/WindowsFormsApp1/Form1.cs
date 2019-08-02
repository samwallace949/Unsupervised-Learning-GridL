using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            int buttonSize = 20, padding = 2, gridOffsetX = 100, gridOffestY = 30;
            InitializeComponent();
            for(int i = 0; i < 7; i++) {
                for (int j = 0; j < 7; j++) {
                    Button b = new Button();
                    this.Controls.Add(b);
                    b.SetBounds(
                        (i * (buttonSize + padding)) + gridOffsetX, 
                        (j * (buttonSize + padding)) + gridOffestY, 
                        buttonSize, 
                        buttonSize);
                    
                }
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
