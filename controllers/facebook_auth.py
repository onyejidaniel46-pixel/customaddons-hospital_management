from odoo import http
import json
import requests

class FacebookAuth(http.Controller):
    
    @http.route('/facebook/login', type='http', auth='public', website=True)
    def facebook_login(self, **kwargs):
        # Facebook App credentials - REPLACE WITH YOUR ACTUAL VALUES
        app_id = 'YOUR_FACEBOOK_APP_ID'
        redirect_uri = 'http://localhost:8069/facebook/callback'
        
        # OAuth URL
        fb_oauth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope=email"
        
        return http.redirect(fb_oauth_url)
    
    @http.route('/facebook/callback', type='http', auth='public', website=True)
    def facebook_callback(self, **kwargs):
        code = kwargs.get('code')
        
        if not code:
            return http.redirect('/web/login')
        
        # Facebook App credentials - REPLACE WITH YOUR ACTUAL VALUES
        app_id = 'YOUR_FACEBOOK_APP_ID'
        app_secret = 'YOUR_FACEBOOK_APP_SECRET'
        redirect_uri = 'http://localhost:8069/facebook/callback'
        
        # Exchange code for access token
        token_url = f"https://graph.facebook.com/v18.0/oauth/access_token?client_id={app_id}&redirect_uri={redirect_uri}&client_secret={app_secret}&code={code}"
        
        try:
            response = requests.get(token_url, timeout=10)
            data = response.json()
            access_token = data.get('access_token')
            
            if not access_token:
                return http.redirect('/web/login')
            
            # Get user info
            user_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
            user_response = requests.get(user_url, timeout=10)
            user_data = user_response.json()
            
            email = user_data.get('email')
            fb_id = user_data.get('id')
            name = user_data.get('name')
            
            if not email:
                return http.redirect('/web/login')
            
            # Search for existing partner by email
            partner = http.env['res.partner'].sudo().search([
                ('email', '=', email)
            ], limit=1)
            
            if partner and partner.user_ids:
                # Login existing user
                db = http.request.db
                login = partner.user_ids[0].login
                http.request.session.authenticate(db, login, '')
                return http.redirect('/web')
            
            # If no user found, redirect to login with message
            return http.redirect('/web/login?facebook_email=' + email)
            
        except Exception as e:
            return http.redirect('/web/login')