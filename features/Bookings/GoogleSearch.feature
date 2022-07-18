Feature: Test for going to goggle

  @create_booking-1 @smoke @health
  Scenario: Verify Goggle can be searched
    Given I go to google
    And I Wait
