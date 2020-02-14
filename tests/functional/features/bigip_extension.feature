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
