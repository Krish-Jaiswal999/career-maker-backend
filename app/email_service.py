"""
Email Service for sending OTP and notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
    
    def send_otp_email(self, recipient_email: str, otp: str, full_name: str = "User") -> bool:
        """
        Send OTP email to user
        
        Args:
            recipient_email: Email to send OTP to
            otp: One-time password code
            full_name: User's full name for personalization
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # If no SMTP credentials, skip email (development mode)
            if not self.sender_email or not self.sender_password:
                print(f"[DEV MODE] OTP for {recipient_email}: {otp}")
                return True
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Password Reset OTP - Career Path Planner"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Text and HTML versions
            text = f"""
Hello {full_name},

You requested to reset your password. Use the following OTP to proceed:

OTP: {otp}

This OTP is valid for 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
Career Path Planner Team
            """
            
            html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
      <h2 style="color: #2c3e50;">Password Reset Request</h2>
      <p>Hello <strong>{full_name}</strong>,</p>
      <p>You requested to reset your password. Use the following OTP to proceed:</p>
      
      <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0;">
        <h1 style="color: #3498db; letter-spacing: 5px; margin: 0;">{otp}</h1>
      </div>
      
      <p style="color: #e74c3c;"><strong>This OTP is valid for 10 minutes.</strong></p>
      <p>If you didn't request this, please ignore this email and your password will remain unchanged.</p>
      
      <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
      <p style="color: #999; font-size: 12px;">
        Career Path Planner Team<br>
        This is an automated email. Please do not reply.
      </p>
    </div>
  </body>
</html>
            """
            
            # Attach both versions
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def send_password_reset_confirmation(self, recipient_email: str, full_name: str = "User") -> bool:
        """
        Send password change confirmation email
        
        Args:
            recipient_email: Email to send confirmation to
            full_name: User's full name
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            if not self.sender_email or not self.sender_password:
                print(f"[DEV MODE] Password reset confirmation sent to {recipient_email}")
                return True
            
            message = MIMEMultipart("alternative")
            message["Subject"] = "Password Changed Successfully - Career Path Planner"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            text = f"""
Hello {full_name},

Your password has been successfully changed. If you didn't make this change, please contact support immediately.

Best regards,
Career Path Planner Team
            """
            
            html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
      <h2 style="color: #2c3e50;">Password Changed Successfully</h2>
      <p>Hello <strong>{full_name}</strong>,</p>
      <p style="color: #27ae60;"><strong>✓ Your password has been successfully changed.</strong></p>
      <p>If you didn't make this change, please <a href="#" style="color: #3498db;">contact support</a> immediately.</p>
      
      <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
      <p style="color: #999; font-size: 12px;">
        Career Path Planner Team<br>
        This is an automated email. Please do not reply.
      </p>
    </div>
  </body>
</html>
            """
            
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True
            
        except Exception as e:
            print(f"Failed to send confirmation email: {str(e)}")
            return False
