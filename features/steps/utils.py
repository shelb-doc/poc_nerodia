import re
import string
from random import random, choices

from behave import *
from time import sleep

from selenium.webdriver import Keys
from strgen import StringGenerator

use_step_matcher("parse")

# Locators
menu_button = {'class': 'navbar-toggler'}
login_button = {'type': 'submit'}


# <editor-fold desc="Basic Steps for Web base Apps">
@step("I go to our app and log in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u'''
        Given I go to our app
        Then The page title should be Stellar MMS
        And Login using the credentials for Admin user
        Then The page title should be Welcome - SERVICE_LINE - MARINA_NAME - Stellar MMS 
    ''')


@step("I go to our app")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    context.browser.goto(context.config.userdata['url'])
    context.browser.cookies.clear()
    context.browser.wd.execute_script('window.sessionStorage.clear()')
    context.browser.wd.execute_script('localStorage.clear()')

    print(f'Opening {context.config.userdata["url"]}\n')


@step("I click the menu button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.button(menu_button).click()


@step("Login using the credentials for Admin user")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Login page objects
    print(f'We Login using the stored credentials for Admin user.\n')
    context.browser.text_field(id='username').clear()
    context.browser.text_field(id='username').send_keys(context.config.userdata["admin_username"])
    context.browser.text_field(id='password').clear()
    context.browser.text_field(id='password').send_keys(context.config.userdata["admin_password"])
    context.browser.button(login_button).click()
    sleep(2)
    context.execute_steps(u'''
        Given I set the dropdown with xpath=//*[@id="main-wrapper"]/nav/div[2]/div/div[1]/span/div/select to be MimikyuTwo
        And I check Location Change Successful is present in the page
        And I save value of the select with xpath=//*[@id="main-wrapper"]/nav/div[2]/div/div[1]/span/div/select as marina_name
        Then I save value of the select with xpath=//*[@id="main-wrapper"]/nav/div[2]/div/div[2]/span/div/select as service_line
    ''')
    print(f'We Login successfully\n')


@step("I browse to {url}")
def step_impl(context, url):
    """
    :type context: behave.runner.Context
    """
    context.browser.goto(url)
    print(f'Opening {url}\n')


@step("I clear the browser's cookies")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.cookies.clear()


@step("The page title should be {title}")
def step_impl(context, title):
    """
    :param title: str, Expected page title
    :type context: behave.runner.Context
    """
    sleep(2)
    context.browser.wait()

    if 'MARINA_NAME' in title:
        title = title.replace('MARINA_NAME', context.fake_user['marina_name'])
    if 'SERVICE_LINE' in title:
        title = title.replace('SERVICE_LINE', context.fake_user['service_line'])
    assert title in context.browser.title.strip(), f"Current Page Title: {context.browser.title}\n" \
                                                   f"Expected Page Title: {title}\n"
    print(f'The Current Page Title: {context.browser.title} matches the '
          f'Expected Page Title: {title}\n')


@step("I check {message} is present in the page")
def step_impl(context, message):
    """
    :param message: Message/text to search for in the page.
    :type context: behave.runner.Context
    """
    if message in context.fake_user:
        assert context.fake_user[message] in context.browser.html, f"Couldn't find {context.fake_user[message]}" \
                                                                   f" in the Web page.\n"
        print(f'{context.fake_user[message]} is present in the page.\n')
    else:
        assert str(message) in context.browser.html, f"Couldn't find {message} in the Web page.\n"
        print(f'The message "{message}" is present in the page.\n')


@step("Verified {message} is in the URL")
def step_impl(context, message):
    """
    :param message: String to search for in the URL
    :type context: behave.runner.Context
    """

    assert message in context.browser.url, f"Couldn't find {message} in {context.browser.url}.\n"
    print(f'{message} is present in the url.\n')


@step("I Wait for the page to load")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    sleep(15)


@step("I Wait")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    sleep(500)


@step("I click the {html_tag} with {selector}={identifier}")
def step_impl(context, html_tag, selector, identifier):
    """
    This step is a catch-all for all basic clicks.
    :param selector: text, id, name, etc.
    :param identifier: text, id, or name, depends on the tag you provide.
    :param html_tag: a, input, button, etc.
    :type context: behave.runner.Context
    """
    context.browser.wait()
    # ADD a dict to make finding objects more dynamic
    kwargs = {selector.lower(): identifier}
    if html_tag.lower() == 'link' or html_tag.lower() == 'a':
        context.browser.link(kwargs).click()
    elif html_tag.lower() == 'input':
        context.browser.input(kwargs).js_click()
    elif html_tag.lower() == 'button':
        context.browser.button(kwargs).click()
    elif html_tag.lower() == 'image':
        context.browser.image(kwargs).click()
    elif html_tag.lower() == 'text':
        context.browser.image(kwargs).click()
    elif html_tag.lower() == 'span':
        context.browser.span(kwargs).click()
    elif html_tag.lower() == 'th':
        context.browser.th(kwargs).click()
    elif html_tag.lower() == 'placeholder':
        context.browser.placeholder(kwargs).click()
    elif html_tag.lower() == 'input':
        context.browser.input(kwargs).click()
    elif html_tag.lower() == 'div':
        context.browser.div(kwargs).click()
        sleep(5)
    elif html_tag.lower() == 'class':
        context.browser.div(kwargs).click()
        sleep(5)
    else:
        assert False, f"No method to handle elements of tag {html_tag}"
    print(f'We click on {identifier}\n')


@step("I validate {html_tag} with {selector}={identifier} is not obscured, else scroll to it")
def step_impl(context, html_tag, selector, identifier):
    """
    This step is a catch-all for all basic clicks.
    :param selector: text, id, name, etc.
    :param identifier: text, id, or name, depends on the tag you provide.
    :param html_tag: a, input, button, etc.
    :type context: behave.runner.Context
    """
    context.browser.wait()
    # ADD a dict to make finding objects more dynamic
    kwargs = {selector.lower(): identifier}
    target = ''
    if html_tag.lower() == 'link' or html_tag.lower() == 'a':
        target = context.browser.link(kwargs)
    elif html_tag.lower() == 'input':
        target = context.browser.input(kwargs)
    elif html_tag.lower() == 'button':
        target = context.browser.button(kwargs)
    elif html_tag.lower() == 'image':
        target = context.browser.image(kwargs)
    elif html_tag.lower() == 'text':
        target = context.browser.image(kwargs)
    elif html_tag.lower() == 'span':
        target = context.browser.span(kwargs)
    elif html_tag.lower() == 'th':
        target = context.browser.th(kwargs)
    elif html_tag.lower() == 'div':
        target = context.browser.div(kwargs)
    else:
        assert False, f"No method to handle elements of tag {html_tag}"
    if target.obscured:
        location = target.center
        print(f'Element center is x={location.x} y={location.y}\n')
        target.scroll.by(location.x + 1000, location.y)
        sleep(100)
        print(f'Element was obscured, We scrolled to {identifier}\n')
    else:
        print(f'Element was not obscured, we do not need to scroll for {identifier}\n')


@step("I type {payload} in the field with {identifier}={value}")
def step_impl(context, payload, identifier, value):
    """
    This step will handle all the typing, should work as long as the html tag is of type input.
    :param payload: What to type, you can also have it create it for you using the random options.
    :param identifier: Type of identifiers. Ex: ID or name.
    :param value: of the Identifier.
    :type context: behave.runner.Context
    """
    kwargs = {identifier.lower(): value}
    if "random" in payload.lower():
        payload = payload.replace('Random ', '')
        if payload == 'First Name':
            context.browser.text_field(kwargs).clear()
            context.browser.text_field(kwargs).send_keys(context.fake.first_name().capitalize())
        elif payload == 'Last Name':
            context.browser.text_field(kwargs).clear()
            context.browser.text_field(kwargs).send_keys(context.fake.last_name().capitalize())
        elif payload == 'Email':
            context.browser.text_field(kwargs).clear()
            context.browser.text_field(kwargs).send_keys(context.fake.email())
        elif payload == 'SSN':
            random_ssn = ''.join(choices(string.digits, k=4))
            context.browser.text_field(kwargs).clear()
            context.browser.text_field(kwargs).send_keys(random_ssn)
        elif payload == 'Phone Number':
            context.browser.text_field(kwargs).clear()
            random_phone_number = ''.join(choices(string.digits, k=10))
            context.browser.text_field(kwargs).send_keys(random_phone_number)
        elif payload == 'Password':
            context.browser.text_field(kwargs).clear()
            context.browser.text_field(kwargs).send_keys(
                StringGenerator(r'[\c]{6:12}&[!#\$]&[\d]&[\u]{2}').render())
        elif payload == 'Username':
            context.browser.text_field(kwargs).clear()
            context.browser.text_field(kwargs).send_keys(context.fake.user_name())
        # This will store this for future uses during the application
        context.fake_user[payload] = context.browser.text_field(kwargs).value
        print(f"{payload} set to {context.fake_user[payload]}\n")
    elif "previous" in payload.lower():
        payload = payload.replace('Previous ', '')
        context.browser.text_field(kwargs).clear()
        context.browser.text_field(kwargs).send_keys(context.fake_user[payload])
        print(f"{payload} set to {context.fake_user[payload]}\n")
    elif "temporary" in payload.lower():
        payload = payload.replace('Temporary ', '')
        if payload == 'Email':
            context.fake_user[payload] = context.temp_email
            context.browser.input(kwargs).send_keys(context.fake_user[payload])
            print(f"{payload} set to {context.fake_user[payload]}\n")
    else:
        context.browser.text_field(kwargs).clear()
        context.browser.text_field(kwargs).send_keys(payload)


@step("I validate that the {html_tag} with {selector}={identifier} has an attribute {name}={value}")
def step_impl(context, html_tag, selector, identifier, name, value):
    """
    This steps allows us to check on attributes in the html code.
    :param html_tag: input, button, etc... (if not set below, please add it)
    :param selector: ID, name, value, etc...
    :param identifier: value of the selector.
    :param name: name of the attribute we are going to check on.
    :param value: expected value in the attribute we pass in the name var.
    :type context: behave.runner.Context
    """
    # ADD a dict to make finding objects more dynamic
    kwargs = {selector.lower(): identifier}
    if html_tag.lower() == 'link' or html_tag.lower() == 'a':
        current_value = context.browser.link(kwargs).get_attribute(name)
    elif html_tag.lower() == 'input':
        current_value = context.browser.input(kwargs).get_attribute(name)
    elif html_tag.lower() == 'image':
        current_value = context.browser.image(kwargs).get_attribute(name)
    elif html_tag.lower() == 'paragraph':
        current_value = context.browser.p(kwargs).get_attribute(name)
    else:
        assert False, f"No method to handle elements of tag {html_tag}"
    assert str(current_value) in str(value), f"The current value of {name} is {current_value}, " \
                                             f"not {value}"
    print(f'The Field {identifier} has an attribute {name} with the value of {current_value} \n')


@step("I validate that the {html_tag} with {selector}={identifier} contains the text {value}")
def step_impl(context, html_tag, selector, identifier, value):
    """
    This steps allows us to check on Text contained.
    :param html_tag: input, button, etc... (if not set below, please add it)
    :param selector: ID, name, value, etc...
    :param identifier: value of the selector.
    :param value: Expected text in the element.
    :type context: behave.runner.Context
    """
    # ADD a dict to make finding objects more dynamic
    kwargs = {selector.lower(): identifier}
    if html_tag.lower() == 'link' or html_tag.lower() == 'a':
        current_value = context.browser.link(kwargs).text
    elif html_tag.lower() == 'input':
        current_value = context.browser.input(kwargs).text
    elif html_tag.lower() == 'span':
        current_value = context.browser.span(kwargs).text
    elif html_tag.lower() == 'div':
        current_value = context.browser.div(kwargs).text
    elif html_tag.lower() == 'placeholder':
        current_value = context.browser.placeholder(kwargs).text
    elif html_tag.lower() == 'paragraph':
        sleep(3)
        current_value = context.browser.p(kwargs).text
    else:
        assert False, f"No method to handle elements of tag {html_tag}"
    assert str(current_value) == str(value), f"The current text of {identifier} is {current_value}, " \
                                             f"not {value}"
    print(f'The Text for {identifier} matches the expected {current_value} \n')


@step("I validate that the image with {selector}={identifier} has loaded correctly")
def step_impl(context, selector, identifier):
    """
    This is used to validate has loaded correct, the way we achieve this is by testing the width of the picture,
    if it's equal to 0 then we will assume it failed to load properly.
    :param selector: ID, name, value, etc...
    :param identifier: value of the selector.
    :type context: behave.runner.Context
    """
    kwargs = {selector.lower(): identifier}
    assert context.browser.image(
        kwargs).loaded is True, f"The image with {selector}={identifier} didn't load correctly!\n"
    print(f"The image with {selector}={identifier} loaded correctly!\n")


@step("I save value of the {html_tag} with {selector}={identifier} as {value}")
def step_impl(context, html_tag, selector, identifier, value):
    """
    This steps allows us to save the value of ann element.
    :param html_tag: input, button, etc...
    :param selector: ID, name, value, etc...
    :param identifier: value of the selector.
    :param value: name to save data under.
    :type context: behave.runner.Context
    """
    # ADD a dict to make finding objects more dynamic
    kwargs = {selector.lower(): identifier}
    if html_tag.lower() == 'link' or html_tag.lower() == 'a':
        current_value = context.browser.link(kwargs).text
    elif html_tag.lower() == 'input':
        current_value = context.browser.input(kwargs).text
    elif html_tag.lower() == 'span':
        current_value = context.browser.span(kwargs).text
    elif html_tag.lower() == 'div':
        current_value = context.browser.div(kwargs).text
    elif html_tag.lower() == 'paragraph':
        sleep(3)
        current_value = context.browser.p(kwargs).text
    elif html_tag.lower() == 'td':
        sleep(3)
        current_value = context.browser.td(kwargs).text
    elif html_tag.lower() == 'select':
        sleep(3)
        current_option = context.browser.select(kwargs).wait_until(method=lambda e: e.present).value
        option_kwargs = {'value': current_option}
        current_value = context.browser.option(option_kwargs).text
    else:
        assert False, f"No method to handle elements of tag {html_tag}"
    # This will store this for future uses during the application
    context.fake_user[value] = current_value
    print(f"{value} set to {context.fake_user[value]}\n")


@step("I press ENTER in the field with {identifier}-{value}")
def step_impl(context, identifier, value):
    """
    This step will handle all the typing, should work as long as the html tag is of type input.
    :param identifier: Type of identifiers. Ex: ID or name.
    :param value: of the Identifier.
    :type context: behave.runner.Context
    """
    kwargs = {identifier.lower(): value}
    context.browser.input(kwargs).send_keys(Keys.ENTER)


@step("I set the dropdown with {selector}={identifier} to be {value}")
def step_impl(context, selector, identifier, value):
    """
    This step will handle all the typing, should work as long as the html tag is of type input.
    :param selector: Type of identifiers. Ex: ID or name.
    :param identifier: of the selector
    :param value: of the Identifier.
    :type context: behave.runner.Context
    """
    kwargs = {selector.lower(): identifier}
    context.browser.select(kwargs).select(value)
