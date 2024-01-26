import os
from dotenv import load_dotenv
from supabase import create_client
from flask import Flask

from .providers import schedule_providers_cron

load_dotenv()

# Initialize the Supabase client
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

# SCHEDULE CRON
schedule_providers_cron(supabase)

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    
    # Set the Supabase client as a config variable
    app.config['SUPABASE'] = supabase
    
    # Register blueprints
    from . import compare
    app.register_blueprint(compare.bp)
    
    # Return the app
    return app