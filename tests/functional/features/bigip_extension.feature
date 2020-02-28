Feature: BIG-IP Extension Client

  Scenario Outline: Install <component> on BIG-IP
    Given we have a BIG-IP available
     When we install <component>
     Then <component> will be installed

    Examples: All Extension Components
        | component |
        | do        |
        | as3       |
        | ts        |
        | cf        |

  Scenario Outline: Get info from <component> on BIG-IP
    Given we have a BIG-IP available
     and <component> is installed
     When we get info from <component>
     Then <component> will return a version

    Examples: All Extension Components
        | component |
        | do        |
        | as3       |
        | ts        |
        | cf        |

  Scenario: Configure Application on BIG-IP using as3
    Given we have a BIG-IP available
     and as3 is installed
     When we configure as3 with a declaration
      """
      {
          "class": "ADC",
          "schemaVersion": "3.0.0",
          "Sample_01": {
              "class": "Tenant",
              "Application_1": {
                  "class": "Application",
                  "template": "http",
                  "serviceMain": {
                      "class": "Service_HTTP",
                      "virtualAddresses": [
                          "10.0.1.100"
                      ],
                      "pool": "web_pool"
                  },
                  "web_pool": {
                      "class": "Pool",
                      "monitors": [
                          "http"
                      ],
                      "members": [
                          {
                              "servicePort": 80,
                              "serverAddresses": [
                                  "192.0.1.10"
                              ]
                          }
                      ]
                  }
              }
          }
      }
      """
     Then a virtual server will be created with address 10.0.1.100

  Scenario: Sending a declaration to TS
    Given we have a BIG-IP available
    and ts is installed
    When we configure ts with a declaration
      """
      {
          "class": "Telemetry",
          "My_System": {
              "class": "Telemetry_System",
              "systemPoller": {
                  "interval": 60
              }
          },
          "My_Listener": {
              "class": "Telemetry_Listener",
              "port": 6514
          },
          "My_Consumer": {
              "class": "Telemetry_Consumer",
              "type": "Splunk",
              "host": "192.0.2.1",
              "protocol": "https",
              "port": 8088,
              "passphrase": {
                  "cipherText": "apikey"
              }
          }
      }
      """
    Then a success message is returned by ts

  Scenario: Sending a declaration to DO
    Given we have a BIG-IP available
     and do is installed
     When we configure do with a declaration
      """
       {
            "class": "DbVariables",
            "ui.advisory.text": "test scenario text"
       }
      """
     Then advisory text will be set to "test scenario text"

  Scenario: Sending a declaration to CF
    Given we have a BIG-IP available
    and cf is installed
    When we configure cf with a declaration
      """
      {
        "class": "Cloud_Failover",
        "environment": "{environment}",
        "externalStorage": {
            "scopingTags": {
                "f5_cloud_failover_label": "{deploymentId}"
            }
        },
        "failoverAddresses": {
            "scopingTags": {
                "f5_cloud_failover_label": "{deploymentId}"
            }
        },
        "failoverRoutes": {
            "scopingTags": {
                "f5_cloud_failover_label": "{deploymentId}"
            },
            "scopingAddressRanges": [
                {
                    "range": "192.168.1.0/24"
                }
            ],
            "defaultNextHopAddresses": {
                "discoveryType": "static",
                "items": [
                    "192.0.2.10",
                    "192.0.2.11"
                ]
            }
        }
      }
      """
    Then a success message is returned by cf

  Scenario Outline: Getting inspect from <component> on BIG-IP
    Given we have a BIG-IP available
    and <component> is installed
    When we get inspect from <component>
    Then <component> will return inspect info

    Examples: Extension Components
      | component |
      | do        |
      | cf        |

  Scenario: Sending a reset to CF
    Given we have a BIG-IP available
    and cf is installed
    When we post reset to cf
    Then cf will validate and return response

  Scenario: Sending a trigger to CF
    Given we have a BIG-IP available
    and cf is installed
    When we post trigger to cf
    Then cf will validate and return response

  Scenario: Getting the state file status from CF
    Given we have a BIG-IP available
    and cf is installed
    When we call get trigger from cf
    Then cf will validate and return response
