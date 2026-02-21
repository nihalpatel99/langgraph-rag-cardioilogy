using System;
using System.Drawing;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CardioApp
{
    public partial class Form1 : Form
    {
        private Label lblHeading;
        private TextBox txtQuery;
        private Button btnSubmit;
        private RichTextBox rtbOutput;

        private readonly HttpClient httpClient = new HttpClient();

        public Form1()
        {
            InitializeUI();
        }

        private void InitializeUI()
        {
            this.Text = "Cardiology AI Assistant";
            this.Size = new Size(900, 600);
            this.StartPosition = FormStartPosition.CenterScreen;

            lblHeading = new Label
            {
                Text = "Cardiology AI Assistant",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                AutoSize = true,
                Top = 20,
                Left = 250,
                ForeColor = Color.DarkBlue
            };

            txtQuery = new TextBox
            {
                Width = 600,
                Height = 30,
                Top = 100,
                Left = 130,
                Font = new Font("Segoe UI", 12)
            };

            btnSubmit = new Button
            {
                Text = "Submit",
                Width = 120,
                Height = 35,
                Top = 150,
                Left = 380,
                BackColor = Color.SteelBlue,
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };

            btnSubmit.Click += async (s, e) => await BtnSubmit_Click();

            rtbOutput = new RichTextBox
            {
                Width = 750,
                Height = 300,
                Top = 220,
                Left = 70,
                Font = new Font("Segoe UI", 11),
                ReadOnly = true,
                BackColor = Color.WhiteSmoke
            };

            this.Controls.Add(lblHeading);
            this.Controls.Add(txtQuery);
            this.Controls.Add(btnSubmit);
            this.Controls.Add(rtbOutput);
        }

        private async Task BtnSubmit_Click()
        {
            string query = txtQuery.Text;

            if (string.IsNullOrWhiteSpace(query))
            {
                MessageBox.Show("Please enter a query.");
                return;
            }

            try
            {
                btnSubmit.Enabled = false;
                rtbOutput.Text = "Loading...\n";

                var requestBody = new
                {
                    query = query
                };

                string json = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                HttpResponseMessage response = await httpClient.PostAsync(
                    "http://localhost:8080/cardio",
                    content
                );

                response.EnsureSuccessStatusCode();

                string responseString = await response.Content.ReadAsStringAsync();

                using JsonDocument doc = JsonDocument.Parse(responseString);
                string aiResponse = doc.RootElement
                                       .GetProperty("response")
                                       .GetString();

                rtbOutput.Text = aiResponse;
            }
            catch (Exception ex)
            {
                rtbOutput.Text = "Error:\n" + ex.Message;
            }
            finally
            {
                btnSubmit.Enabled = true;
            }
        }

        
    }
}