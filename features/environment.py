# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
"""
before_step(context, step), after_step(context, step)
    These run before and after every step.
    The step passed in is an instance of Step.
before_scenario(context, scenario), after_scenario(context, scenario)
    These run before and after each scenario is run.
    The scenario passed in is an instance of Scenario.
before_feature(context, feature), after_feature(context, feature)
    These run before and after each feature file is exercised.
    The feature passed in is an instance of Feature.
before_tag(context, tag), after_tag(context, tag)
"""
from behave import use_step_matcher
from faker import Factory
from faker.providers import company, internet
from nerodia.browser import Browser
from selenium.webdriver.chrome.options import Options as chrome_options

# -- SETUP: Use cfparse as default matcher
use_step_matcher('cfparse')


def before_all(context):
    # We Generate a Fake set of data and add different sets of data.
    context.fake = Factory.create()
    context.fake.add_provider(company)
    context.fake.add_provider(internet)


def before_scenario(context, scenario):
    # Start browser
    options = chrome_options()
    # options = firefox_options()
    # options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--private")
    # options.add_argument("--headless")
    # context.browser = webdriver.Edge()
    context.browser = Browser(browser='chrome', options=options)
    context.browser.window().maximize()
    # We create a dict to store the data of the fake user
    context.fake_user = dict()
    # Print which scenario we are about to test
    print(f'Starting test for {scenario.tags[0]}: {context.scenario.name}\n')


def after_scenario(context, scenario):
    # Bring Global Variable for JIRA API
    context.browser.close()
    print(f'Finished test for {scenario.tags[0]}: {context.scenario.name}\n')
