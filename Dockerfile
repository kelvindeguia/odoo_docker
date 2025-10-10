# Start from official Odoo 18 image
FROM odoo:18.0

# Set working directory inside container
WORKDIR /mnt/extra-addons

# Copy your custom addons (if you have a folder named addons)
COPY ./addons /mnt/extra-addons

# Copy config file if available
COPY ./odoo.conf /etc/odoo/odoo.conf

# Expose Odoo default port
EXPOSE 8069

# Run Odoo with config
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
