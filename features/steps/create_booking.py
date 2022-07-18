from time import sleep

from behave import *

use_step_matcher("parse")

# Locators
create_booking_drop = {'text': 'Bookings'}
create_booking_endpoint = {'href': '/booking/add'}
find_customer = {'text': 'Find Customer'}
save_booking = {'text': 'Save Booking'}

# Customers
customer_657 = {'class': 'id-cell'}

# Input Locators
contract_type = {'id': 'contractType'}
contract_date_start = {'id': 'startDate'}
contract_date_end = {'id': 'endDate'}
season_contract = {'id': 'contractSeason'}
unit_type = {'id': 'units.0.unitType'}
unit_name = {'id': 'units.0.unit'}
customer_id = {'placeholder': 'Search CUSTOMER ID'}
boat_classification = {'id': 'units.0.classification'}
payment_freq = {'id': 'units.0.paymentFrequency'}
option_select = {'id': 'unit-1'}
option_submit = {'text': 'Submit'}

# delete and cancel
delete_booking = {'text': 'Delete Booking'}
confirm_delete = {'text': 'Confirm'}
cancel_booking = {'text': 'Cancel Booking'}
confirm_cancel = {'text': 'Submit'}
confirm_save = {'text': 'Confirm'}


@step("I open the Create Booking page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u'''
        given I click the menu button
        then I click the span with text=''' + create_booking_drop['text'] + u'''
        then I click the link with href=''' + create_booking_endpoint['href'])


@step("I click the find customer button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u'''
        given i click the span with text=''' + find_customer['text'])
    sleep(4)


@step("I click the customer with the id of #657")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u'''
        given I type 657 in the field with placeholder=''' + customer_id['placeholder'])
    sleep(5)
    context.execute_steps(u'''
        Given I click the div with class=''' + customer_657['class'])


@step("I set up Transient contract type and dates")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u'''
        given I type Transient in the field with id=''' + contract_type['id'] + u'''
        and I press ENTER in the field with id-''' + contract_type['id'] + u'''
        then I type 3/01/22 in the field with id=''' + contract_date_start['id'] + u'''
        and i click the div with class=header-menu-bars''')
    context.execute_steps(u'''
        given I type 3/31/22 in the field with id=''' + contract_date_end['id'] + u'''
        and i click the div with class=header-menu-bars''')


@step("I set the A-101 unit and unit type")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(f'''
        given I type A-101 in the field with id={unit_name['id']}
        and I press ENTER in the field with id-{unit_name['id']}
        then I type Covered in the field with id={unit_type['id']}
        and I press ENTER in the field with id-{unit_type['id']}''')


@step("I set the Payment Frequency to One Time")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(f'''
        given I type One Time in the field with id={payment_freq['id']}
        and I press ENTER in the field with id-{payment_freq['id']}''')


@step("I select the Unit Line and Accessory Line options with Flat Rate")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(f'''
        given I set the dropdown with id=unit-1 to be 063b9552-533b-4b65-9bb8-d8d1cd1208da
        and I set the dropdown with id=accessory-1 to be af3b70cf-6066-42dd-b670-88bfcc7a868e
        and I click the span with text={option_submit['text']}''')
    sleep(3)


@step("I save the booking")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(f'''
        given I click the span with text={save_booking['text']}''')
    sleep(9)