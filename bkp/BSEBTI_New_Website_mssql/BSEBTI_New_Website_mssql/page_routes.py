from flask import Flask, render_template,request,session, jsonify
import mysql.connector

from __main__ import app


import pymssql
from config import Config



###############################################
BROCHURE_DIRECTORY ='static'
# BROCHURE_FILENAME='BMS-in-Capital-Markets.pdf'
BROCHURE_FILENAME=''

# Database configuration
# db_config = {
#     'user': 'root',
#     'password': '',
#     'host': 'localhost',
#     'database': 'enquiry_db'
# }

app.config.from_object(Config)

def get_db_connection():
    conn = pymssql.connect(
        server=app.config['SQL_SERVER'],
        user=app.config['SQL_USERNAME'],
        password=app.config['SQL_PASSWORD'],
        database=app.config['SQL_DATABASE']
    )
    return conn


# Temporary storage for OTPs
otp_store = {}
###############################################


############ Sample Test ####################
# @app.route('/test', methods=['GET'])
# def test():
#     return 'it works!'

@app.route('/header', methods=['GET'])
def header():
    return render_template('header.html')


@app.route('/footer', methods=['GET'])
def footer():
    return render_template('footer.html')

################################### Add To Cart Routes Start ##############################
@app.route('/add_to_cart', methods=['GET','POST'])
def add_to_cart():
    # enroll_btn_val=request.form
    print('session')
    print(session)

    # session['enroll_now_btn'] = request.form['enroll_now_btn']
    enroll_btn_vals = request.form['enroll_now_btn']
    enroll_btn_val= enroll_btn_vals
    # textbox_value = session.get('textbox_value', '')
    # enroll_btn_val= session['enroll_now_btn','']
    # print('enroll_btn_val session')
    # # print('session')
    # print(session)
    # print('enroll_btn_val after assign')
    # print(enroll_btn_val)
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM course_names WHERE id='+enroll_btn_val
    cursor.execute(query)
    fet_course_name = cursor.fetchall()
    print('fet_course_name')
    print(fet_course_name[0][1])
    cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    # query1 ="SELECT * FROM qualifications"
    # cursor1.execute(query1)
    # # cursor1.close()
    # # all_cities = cursor.fetchall()
    # qualifications = cursor1.fetchall()
    # # print(all_cities)
    return render_template('cart.html',course_name=fet_course_name[0],enroll_btn_val=enroll_btn_val)
    # return render_template('cart.html',course_name=fet_course_name[0])

@app.route('/checkout_page', methods=['GET','POST'])
def checkout_page():
    checkout_btn_val=request.form['checkout_btn']
    # enroll_btn_val = request.form['enroll_now_btn']
    # print('enroll_btn_val')
    # print(enroll_btn_val)
    # connection = mysql.connector.connect(**db_config)
    # cursor = connection.cursor()
    # query = 'SELECT * FROM course_names WHERE id='+enroll_btn_val
    # cursor.execute(query)
    # fet_course_name = cursor.fetchall()
    # print('fet_course_name')
    # print(fet_course_name[0][1])
    # cursor.close()

    # cursor1 = connection.cursor(buffered=True)
    # query1 ="SELECT * FROM qualifications"
    # cursor1.execute(query1)
    # # cursor1.close()
    # # all_cities = cursor.fetchall()
    # qualifications = cursor1.fetchall()
    # # print(all_cities)
    return render_template('checkout.html',checkout_details=checkout_btn_val)##,course_name=fet_course_name[0])


@app.route('/fees_types', methods=['GET'])

def get_fees_types():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    # cur = mysql.connection.cursor()
    cur = connection.cursor()
    cur.execute("SELECT id,fees_name,fees_amount FROM fees_types")
    fees_types = [dict(id=row[0],fees_name=row[1]) for row in cur.fetchall()]
    cur.close()
    return jsonify(fees_types)

@app.route('/fees_names', methods=['GET'])

def get_fees_names():
    fees_types = request.args.get('fees_types') ######## Textbox id
    # print('courses_types')
    # print(courses_types)
    # cur = mysql.connection.cursor()
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cur = connection.cursor()
    # Get country_id
    cur.execute("SELECT id,fees_name,fees_amount FROM fees_types WHERE id = %s", [fees_types]) #### 
    fees_name_id = cur.fetchone()
    print(fees_name_id)

    # if fees_name_id:
    #     course_type_id = course_type_id[0]
    #     # Get states for the country
    #     cur.execute("SELECT id,fees_name FROM fees_types WHERE id = %s", [course_type_id])
    #     # states = [course_name[0] for course_name in cur.fetchall()]
    #     states = [dict(course_name_id=courses_name[0],course_name=courses_name[1]) for courses_name in cur.fetchall()]
    # else:
    #     states = []
    cur.close()
    return jsonify(fees_name_id)
    # return jsonify(states)
################################### Add To Cart Routes End ##############################

################################### My Courses Page Start #####################################
@app.route('/my_courses', methods=['GET'])
def my_courses():
    return render_template('my_courses.html')

################################### My Courses Page End #####################################


################################### Main Page Routes Start ############################
@app.route('/graduate_courses', methods=['GET'])
def graduate_courses():
    return render_template('graduate.html')

@app.route('/post_graduate_courses', methods=['GET'])
def post_graduate_courses():
    return render_template('post-graduate.html')

@app.route('/professional_studies', methods=['GET'])
def professional_studies():
    return render_template('professional-studies.html')

@app.route('/vocational_courses', methods=['GET'])
def vocational_courses():
    return render_template('vocational.html')

@app.route('/profx_courses', methods=['GET'])
def profx_courses():
    return render_template('profx.html')

@app.route('/microx_courses', methods=['GET'])
def microx_courses():
    return render_template('microx.html')

################################### Main Page Routes End ############################

################################### Graduate Courses Routes Start ############################
@app.route('/bms_in_capital_markets', methods=['GET'])
def bms_in_capital_markets():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/graduate/BMS-in-Capital-Markets.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/bba_marketing_and_financial_services_analytics', methods=['GET'])
def bba_marketing_and_financial_services_analytics():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('graduate/BBA-Banking-and-Financial-Services-Analytics.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/bsc_in_data_science', methods=['GET'])
def bsc_in_data_science():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/graduate/BSc-in-Data-Science.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/bsc_in_finance', methods=['GET'])
def bsc_in_finance():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/graduate/BSc-in-Finance.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/bba_in_financial_markets', methods=['GET'])
def bba_in_financial_markets():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/graduate/BBA-in-Financial-Markets.html', all_cities=all_cities, qualifications=qualifications)
################################### Graduate Courses Routes End ############################

################################### Post Graduate Courses Routes Start ############################
@app.route('/pg_diploma_in_global_financial_markets', methods=['GET'])
def pg_diploma_in_global_financial_markets():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/post-graduate/post-graduate-diploma-in-global-financial-markets.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pg_diploma_in_cyber_security', methods=['GET'])
def pg_diploma_in_cyber_security():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('post-graduate/Post-Graduate-Diploma-in-Cyber-Security.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pg_diploma_in_predictive_analytics', methods=['GET'])
def pg_diploma_in_predictive_analytics():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/post-graduate/post-graduate-diploma-in-predictive-analytics.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pg_diploma_in_financial_technology', methods=['GET'])
def pg_diploma_in_financial_technology():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/post-graduate/post-graduate-diploma-in-financial-technology.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pg_program_in_banking_and_finance', methods=['GET'])
def pg_program_in_banking_and_finance():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/post-graduate/post-graduate-program-in-banking-and-finance.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pg_diploma_in_regulatory_compliance_management', methods=['GET'])
def pg_diploma_in_regulatory_compliance_management():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('post-graduate/post-graduate-diploma-in-regulatory-compliance-management.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pg_diploma_in_financial_markets_makaut', methods=['GET'])
def pg_diploma_in_financial_markets_makaut():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/post-graduate/post-graduate-diploma-in-financial-markets-makaut.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/mba_in_securities_markets_makaut_nshm', methods=['GET'])
def mba_in_securities_markets_makaut_nshm():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/post-graduate/mba-in-securities-markets-makaut-nshm.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/llm_in_insolvency_law', methods=['GET'])
def llm_in_insolvency_law():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/post-graduate/llm-in-insolvency-law.html', all_cities=all_cities, qualifications=qualifications)
################################### Post Graduate Courses Routes End ############################

################################### Professional Courses Routes Start ############################

@app.route('/pc_certified_investment_and_stock_market_expert', methods=['GET'])
def pc_certified_investment_and_stock_market_expert():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('professional-courses/certified-investment-and-stock-market-expert.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pc_cexecutive_program_in_securities_and_business_law', methods=['GET'])
def pc_cexecutive_program_in_securities_and_business_law():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/professional-courses/executive-program-in-securities-and-business-law.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pc_cexecutive_program_in_wealth_management', methods=['GET'])
def pc_cexecutive_program_in_wealth_management():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/professional-courses/executive-program-in-wealth-management.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pc_cexecutive_program_in_financial_journalism', methods=['GET'])
def pc_cexecutive_program_in_financial_journalism():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/professional-courses/executive-program-in-financial-journalism.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pc_cexecutive_program_in_risk_management', methods=['GET'])
def pc_cexecutive_program_in_risk_management():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/professional-courses/executive-program-in-risk-management.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/pc_certified_market_analyst_program', methods=['GET'])
def pc_certified_market_analyst_program():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/professional-courses/certified-market-analyst-program.html', all_cities=all_cities, qualifications=qualifications)

################################### Professional Courses Routes End ############################


################################### Vocational Courses Routes Start ############################

@app.route('/vc_global_financial_markets_professional_program_mumbai', methods=['GET'])
def vc_global_financial_markets_professional_program_mumbai():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('vocational-courses/gfmp-global-financial-markets-professional-program-mumbai.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/vc_global_financial_markets_professional_program_kolkata', methods=['GET'])
def vc_global_financial_markets_professional_program_kolkata():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/vocational-courses/gfmp-global-financial-markets-professional-program-Kolkata.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/vc_global_financial_markets_professional_program_delhi', methods=['GET'])
def vc_global_financial_markets_professional_program_delhi():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/vocational-courses/gfmp-global-financial-markets-professional-program-delhi.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/vc_global_data_science_program', methods=['GET'])
def vc_global_data_science_program():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/vocational-courses/global-data-science-program.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/vc_certificate_program_in_investment_banking_operations_classroom', methods=['GET'])
def vc_certificate_program_in_investment_banking_operations_classroom():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/vocational-courses/certificate-program-in-investment-banking-operations.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/vc_certificate_program_in_investment_banking_operations_online', methods=['GET'])
def vc_certificate_program_in_investment_banking_operations_online():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/vocational-courses/certificate-program-in-investment-banking-operations-online.html', all_cities=all_cities, qualifications=qualifications)

################################### Professional Courses Routes End ############################


################################### PROFX Courses Routes Start ############################

@app.route('/profx_advanced_derivatives_market_strategies', methods=['GET'])
def profx_advanced_derivatives_market_strategies():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/vocational-courses/gfmp-global-financial-markets-professional-program-mumbai.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_advanced_forex_trading_strategies', methods=['GET'])
def profx_advanced_forex_trading_strategies():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/profx/advanced-forexs-trading-strategies.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_basic_program_on_stock_markets', methods=['GET'])
def profx_basic_program_on_stock_markets():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/profx/basic-program-on-stock-markets.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_blockchain_for_business_leaders', methods=['GET'])
def profx_blockchain_for_business_leaders():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/profx/blockchain-for-business-leaders.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_capital_markets_bootcamp', methods=['GET'])
def profx_capital_markets_bootcamp():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/profx/capital-markets-bootcamp.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_certificate_program_on_anti_money_laundering', methods=['GET'])
def profx_certificate_program_on_anti_money_laundering():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    print('all_cities')
    print(all_cities)
    # cursor.close()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    # cursor1.close()
    # all_cities = cursor.fetchall()
    qualifications = cursor1.fetchall()
    # print(all_cities)
    return render_template('/profx/Certificate-Program-on-Anti-Money-Laundering.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_certificate_program_on_credit_analysis', methods=['GET'])
def profx_certificate_program_on_credit_analysis():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/certificate-program-on-credit-analysis.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_certificate_program_on_investment_banking', methods=['GET'])
def profx_certificate_program_on_investment_banking():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Certificate-Program-on-Investment-Banking.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_certificate_program_on_stock_market', methods=['GET'])
def profx_certificate_program_on_stock_market():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Certificate-Program-on-Stock-Market.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_certificate_program_on_technical_analysis', methods=['GET'])
def profx_certificate_program_on_technical_analysis():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/certificate-program-on-technical-analysis.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_commodities_and_currency_trading_strategies', methods=['GET'])
def profx_commodities_and_currency_trading_strategies():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Commodities-and-Currency-Trading-Strategies.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_comprehensive_investing_strategies_for_capital_markets', methods=['GET'])
def profx_comprehensive_investing_strategies_for_capital_markets():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Comprehensive-Investing-Strategies-for-Capital-Markets.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_factoring_for_effective_cash_management', methods=['GET'])
def profx_factoring_for_effective_cash_management():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/factoring-for-effective-cash-management.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_finance_for_business_leaders', methods=['GET'])
def profx_finance_for_business_leaders():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Finance-For-Business-Leaders.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_financial_statment_analysis_using_excel', methods=['GET'])
def profx_financial_statment_analysis_using_excel():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Financial-Statement-Analysis-Using-Excel.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_highspeed_trading_with_algorithms', methods=['GET'])
def profx_highspeed_trading_with_algorithms():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/highspeed-trading-with-algorithms.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_mergers_and_acquisitions_strategies_and_execution', methods=['GET'])
def profx_mergers_and_acquisitions_strategies_and_execution():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('profx/Mergers-and-Acquisitions-Strategies-and-Execution.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_option_chain_strategies_for_intraday_trading', methods=['GET'])
def profx_option_chain_strategies_for_intraday_trading():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Option-Chain-Strategies-for-Intraday-Trading.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_orevival_of_companies_under_the_insolvency_and_bankruptcy', methods=['GET'])
def profx_orevival_of_companies_under_the_insolvency_and_bankruptcy():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Revival-Of-Companies-Under-The-Insolvency-And-Bankruptcy-Code.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_using_financial_modelling_for_analysis_and_valuation', methods=['GET'])
def profx_using_financial_modelling_for_analysis_and_valuation():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/Using-Financial-Modelling-for-Analysis-and-Valuation.html', all_cities=all_cities, qualifications=qualifications)

@app.route('/profx_certificate_program_advanced_treasury_and_foreign_exchange_risk_management', methods=['GET'])
def profx_certificate_program_advanced_treasury_and_foreign_exchange_risk_management():
    # connection = mysql.connector.connect(**db_config)
    connection = get_db_connection()

    cursor = connection.cursor()
    query = 'SELECT * FROM cities'
    cursor.execute(query)
    all_cities = cursor.fetchall()
    # cursor1 = connection.cursor(buffered=True)
    cursor1 = connection.cursor()
    query1 ="SELECT * FROM qualifications"
    cursor1.execute(query1)
    qualifications = cursor1.fetchall()
    return render_template('/profx/certificate-programon-advanced-treasury-and-oreign-exchange-risk-management.html', all_cities=all_cities, qualifications=qualifications)


################################### PROFX Courses Routes End ############################