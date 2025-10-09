from odoo import http
from odoo.http import Controller, request, route, Response

class WebsiteFormController(http.Controller):
    @http.route('/web-form-test/', type='http', auth="public", website=True)
    def website_form(self, **post):
        # Render the form template again
        return http.request.render('website_demo.web_form_test_template')
    
    @http.route('/web-form-test/website_thanks/', type='http', auth="public", methods=['POST'], website=True)
    def submit_web_form(self, **post):
        # Extract form data from the POST request
        name = post.get('name')
        age = post.get('age')
        description = post.get('description')

        # Create a new record in the 'web.form' model
        request.env['web.form'].sudo().create({
            'name': name,
            'age': age,
            'description': description,
        })

        # Return a simple response or redirect to a thank you page
        return http.request.render("website_demo.web_form_website_thanks_test_template")
    
class GraceWebsite(http.Controller):
    @http.route('/grace-panget/', type='http', auth="public", website=True)
    def website_form(self, **post):
        # Render the form template again
        return http.request.render('website_demo.grace_panget_template')

    
    