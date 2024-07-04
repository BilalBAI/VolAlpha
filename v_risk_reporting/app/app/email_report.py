import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send the email report


def send_email_report(receiver_email, total_requirement, largest_loss, macro_scenario_description):
    # Email credentials and settings
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    smtp_server = "smtp.example.com"
    smtp_port = 587

    # Email content
    subject = "Equity Risk Stress Testing Report"
    body = f"""
    <html>
    <head>
        <style>
            body {{font-family: Arial, sans-serif; color: #333;}}
            h1 {{color: #0056b3;}}
            h2 {{color: #333;}}
            table {{width: 100%; border-collapse: collapse; margin: 20px 0;}}
            table, th, td {{border: 1px solid #ddd; padding: 8px;}}
            th {{background-color: #f2f2f2;}}
        </style>
    </head>
    <body>
        <h1>Equity Risk Stress Testing Report</h1>
        <p>Dear Team,</p>
        <p>Please find below the results of the recent equity risk stress testing:</p>

        <h2>Overview</h2>
        <p>The portfolio stress test determines the minimum risk-based requirement for clients, measuring risk exposures at both individual security and portfolio levels.</p>

        <h2>Risk Requirement Aggregation</h2>
        <p>Total requirement is calculated as the sum of the two largest losses from equities, credit, convertible bonds, interest rates, foreign exchange, and commodities, plus the SRSS of remaining stress losses and default charges. The calculated total requirement is <strong>{total_requirement}</strong>.</p>

        <h2>Equity Stress Test Overview</h2>
        <ul>
            <li><strong>Directionality:</strong> Macro and single name shocks, relative value spot and volatility surface shocks.</li>
            <li><strong>Concentration Dislocation:</strong> Delta liquidation risk, sector shocks, seven names, relative value volatility, and vega liquidation risk.</li>
        </ul>

        <h2>Stress Test Scenarios</h2>
        <p><strong>Macro Stress:</strong> Global, country, and asset-specific shocks applied in sequence.</p>

        <table>
            <tr>
                <th>Scenario</th>
                <th>Description</th>
                <th>Largest Loss</th>
            </tr>
            <tr>
                <td>Global Level</td>
                <td>Apply a global shock to all assets.</td>
                <td>{largest_loss['global']}</td>
            </tr>
            <tr>
                <td>Country Dispersions</td>
                <td>Apply positive and negative country dispersion stresses at each global shock node.</td>
                <td>{largest_loss['country']}</td>
            </tr>
            <tr>
                <td>Asset Dispersions</td>
                <td>Apply positive and negative stresses at country dispersion nodes to create four additional stress nodes.</td>
                <td>{largest_loss['asset']}</td>
            </tr>
        </table>

        <p>The largest loss from Global + Country Dispersion + Asset Dispersion will be the dominant macro scenario. Asset dispersion does not apply to companies with a market cap greater than $150 billion.</p>

        <p><strong>Macro Scenario Description:</strong> {macro_scenario_description}</p>

        <p>Best regards,<br/>Risk Management Team</p>
    </body>
    </html>
    """

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Example usage with some dummy data
total_requirement = "$50,000,000"
largest_loss = {
    'global': "$15,000,000",
    'country': "$20,000,000",
    'asset': "$10,000,000"
}
macro_scenario_description = "The dominant macro scenario involves significant global shocks, country-specific stresses, and asset-specific stresses leading to substantial losses."

send_email_report("receiver_email@example.com", total_requirement,
                  largest_loss, macro_scenario_description)
