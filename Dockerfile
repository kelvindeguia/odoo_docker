# Start from official Odoo 18 image
FROM odoo:18.0

# Set working directory inside the container
WORKDIR /mnt/extra-addons

# Copy your custom addons into the container
# (assumes you have an /addons folder in your GitHub repo)
COPY ./addons /mnt/extra-addons

# Copy Odoo configuration file (optional, only if you maintain it in repo)
# Make sure your repo has odoo.conf at the root
COPY ./odoo.conf /etc/odoo/odoo.conf

# Expose the default Odoo port
EXPOSE 8069

# Run Odoo with config file on startup
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
