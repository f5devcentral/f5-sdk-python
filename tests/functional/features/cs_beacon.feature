Feature: Cloud Services Beacon Client

  Scenario: Listing Beacon insights
    Given we have a Cloud services account with beacon subscription
    When we list insights
    Then insights will be listed

  Scenario Outline: Creating a Beacon insight
    Given we have a Cloud services account with beacon subscription
    When we create an insight with a declaration
      """
       {
          "title":"foo",
          "description":"My description",
          "category":"INS_CAT_COST",
          "severity":"INS_SEV_CRITICAL"
      }
      """
    Then an insight with <description> exists

    Examples: Insight Description
      | description      |
      | My description   |

  Scenario Outline: Updating a Beacon insight
    Given we have a Cloud services account with beacon subscription
    When we update an insight with a declaration
      """
       {
          "title":"foo",
          "description":"My updated description",
          "category":"INS_CAT_COST",
          "severity":"INS_SEV_CRITICAL"
      }
      """
    Then an insight with <description> exists

    Examples: Insight Description
      | description              |
      | My updated description   |

  Scenario: Deleting an insight
    Given we have a Cloud services account with beacon subscription
    When we delete a insight with title:foo
    Then the insight with title:foo will be deleted

  Scenario: Listing Beacon insights
    Given we have a Cloud services account with beacon subscription
    When we list insights
    Then insights will be listed

  Scenario: Creating a Beacon application
    Given we have a Cloud services account with beacon subscription
    When we create an application with a declaration
      """
       {
          "action":"deploy",
          "declaration":[
            {
              "application":{
                "name": "test_application",
                "description": "test_description",
                "labels":{
                  "test_label": "test_label_value"
                },
                "dependencies":[],
                "metrics":[]
              }
            }
          ]
      }
      """
    Then an application named "test_application" will exist

  Scenario: Creating a Beacon token
    Given we have a Cloud services account with beacon subscription
    When we create a token with a declaration
      """
       {
          "name": "BIGIP1Token",
          "description": "Token for BIG-IP1"
        }
      """
    Then a token named "BIGIP1Token" is created

  Scenario: Listing Beacon tokens
    Given we have a Cloud services account with beacon subscription
    When we list tokens
    Then tokens will be listed

  Scenario: Deleting an Beacon token
    Given we have a Cloud services account with beacon subscription
    When we delete a token with name "BIGIP1Token"
    Then the token with name "BIGIP1Token" will be deleted

