# Instructions

## Steps

1. Install Splunk Enterprise.
2. Install the Splunk Add-on Builder app by going to Apps -> Find more apps.
3. Go to the Splunk Add-on Builder app and create a new add-on.
4. Go to configure data collection.
5. Create a new input.
6. Select Python code.
7. In data input parameters, add inputs for `app_id` and `app_secret`.
8. In the code editor, add Python code in [input.py](./input.py).
9. Go to your newly created app.
10. Create input. Add `app_id` and `app_secret` from the custom integrations page. Select interval and index.
11. Go to the search tab and search `index="main"`.

## Search for interesting events like

## Add-on features
- Automatically sync logs every x seconds
- Use ID and checkpointing to understand which logs have already been added and doesn’t add duplicate logs
- Use data model to give structure to data and make it more searchable
