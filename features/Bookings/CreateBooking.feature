Feature: Test for validate functionality of the Create Booking page.

  @create_booking-1 @smoke @health
  Scenario: Verify Create Booking page loads correctly
    Given I go to our app and log in
    And I open the Create Booking page
    Then The page title should be Booking - SERVICE_LINE - MARINA_NAME - Stellar MMS

  @create_booking-2
  Scenario: Verify Create a One Time Transient Booking is done with existing customer also cancels said booking
    Given I go to our app and log in
    And I open the Create Booking page
    Then The page title should be Booking - SERVICE_LINE - MARINA_NAME - Stellar MMS
    And I click the find customer button
    Then I click the customer with the id of #657
    And I set up Transient contract type and dates
    Then I set the A-101 unit and unit type
    Then I set the Payment Frequency to One Time
    And I Wait for the page to load
    Then I select the Unit Line and Accessory Line options with Flat Rate
    And I save the booking