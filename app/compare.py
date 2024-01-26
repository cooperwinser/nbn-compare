from flask import Blueprint, request, current_app, session, render_template, redirect, url_for, jsonify

bp = Blueprint('compare', __name__, url_prefix='/compare')

@bp.route('/', methods=['GET', 'POST'])
def index():
    # Get the Supabase client from the app config
    supabase = current_app.config['SUPABASE']
    
    # Get the plans from the database
    plans = supabase.table('plan').select('*, promotion(*), provider(*)').order('price', desc=False).execute()
    plans = plans.data
    
    # Get the products from the database
    products = supabase.table('product').select('*').execute()
    products = products.data
    
    # Get the providers from the database
    providers = supabase.table('provider').select('*').order('provider_name', desc=False).execute()
    providers = providers.data
    
    # Render the template
    return render_template('compare/index.html', plans=plans, products=products, providers=providers)

@bp.route('/filter', methods=['GET'])
def filter():
    # Get the Supabase client from the app config
    supabase = current_app.config['SUPABASE']
    
    # Set the product to get plans for
    provider = request.args.get('provider')
    product = request.args.get('product')
    promotion = request.args.get('promotion')
    
    # Set up the base query
    base_query = supabase.table('plan').select('*, promotion(*), provider(*)').order('price', desc=False)
    
    # Filter the plans
    if provider:
        base_query = base_query.filter('provider', 'eq', provider)
    if product:
        base_query = base_query.filter('product', 'eq', product)
    if promotion == "yes":
        base_query = base_query.gte('promotion', 0)
    if promotion == "no":
        base_query = base_query.is_('promotion', 'null')
    
    # Execute the query
    plans = base_query.order('price', desc=False).execute()
    plans = plans.data
    
    # Return a new table body with the plans
    return render_template('compare/partials/plans_table.html', plans=plans)