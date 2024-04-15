# Template Settings
# ------------------------------------------------------------------------------


# Theme layout templates directory

# Template config
# ? Easily change the template configuration from here
# ? Replace this object with template-config/demo-*.py file's TEMPLATE_CONFIG to change the template configuration as per our demos
TEMPLATE_CONFIG = {
    "layout": "horizontal",             # Options[String]: vertical(default), horizontal
    "theme": "theme-default",         # Options[String]: theme-default(default), theme-bordered, theme-semi-dark
    "style": "light",                 # Options[String]: light(default), dark, system mode
    "rtl_support": True,              # options[Boolean]: True(default), False # To provide RTLSupport or not
    "rtl_mode": False,                # options[Boolean]: False(default), True # To set layout to RTL layout  (myRTLSupport must be True for rtl mode)
    "has_customizer": False,           # options[Boolean]: True(default), False # Display customizer or not THIS WILL REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WON'T WORK
    "display_customizer": True,       # options[Boolean]: True(default), False # Display customizer UI or not, THIS WON'T REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WILL WORK
    "content_layout": "wide",      # options[String]: 'compact', 'wide' (compact=container-xxl, wide=container-fluid)
    "navbar_type": "fixed",           # options[String]: 'fixed', 'static', 'hidden' (Only for vertical Layout)
    "header_type": "fixed",           # options[String]: 'static', 'fixed' (for horizontal layout only)
    "menu_fixed": True,               # options[Boolean]: True(default), False # Layout(menu) Fixed (Only for vertical Layout)
    "menu_collapsed": False,          # options[Boolean]: False(default), True # Show menu collapsed, Only for vertical Layout
    "footer_fixed": False,            # options[Boolean]: False(default), True # Footer Fixed
    "show_dropdown_onhover": True,    # True, False (for horizontal layout only)
    "customizer_controls": [
        "rtl",
        "style",
        "headerType",
        "contentLayout",
        "layoutCollapsed",
        "showDropdownOnHover",
        "layoutNavbarOptions",
        "themes",
    ],  # To show/hide customizer options
}



# Theme Variables
# ? Personalize template by changing theme variables (For ex: Name, URL Version etc...)
THEME_VARIABLES = {
    "creator_name": "Greats Systems",
    "creator_url": "https://greats.systems/",
    "template_name": "SimplyLedgers",
    "template_suffix": "SimplyLedgers ERP",
    "template_version": "1.1.0",
    "template_free": False,
    "template_description": "SimplyLedgers solutions solve primary production problems at farm level to anticipated logistics problems that may arise in the agriculture value chain by utilizing blockchain and IOT technologies. We aim to transform agriculture enabled communities by improving social information flow between communities,enabling business processes from production to logistics to last person in the value chain and integrated data distribution in the agriculture space. ",
    "template_keyword": "primary production problems, farm logistics, logistics, agriculture,  agriculture value chain, blockchain, IOT technologies",
    "facebook_url": "https://www.facebook.com/simplyledgers/",
    "twitter_url": "https://twitter.com/simplyledgers",
    "github_url": "https://github.com/simplyledgers",
    "dribbble_url": "https://dribbble.com/simplyledgers",
    "instagram_url": "https://www.instagram.com/simplyledgers/",
    "license_url": "https://themeforest.net/licenses/standard",
    "live_preview": "https://demos.simplyledgers.com/materialize-html-django-admin-template/demo-1/",
    "product_page": "https://1.envato.market/materialize_admin",
    "support": "https://simplyledgers.ticksy.com/",
    "more_themes": "https://1.envato.market/simplyledgers_portfolio",
    "documentation": "https://demos.simplyledgers.com/materialize-html-admin-template/documentation/django-introduction.html",
    "changelog": "https://demos.simplyledgers.com/vuexy/changelog.html",
    "git_repository": "materialize-html-django-admin-template",
    "git_repo_access": "https://tools.simplyledgers.com/github/github-access",
}

# ! Don't change THEME_LAYOUT_DIR unless it's required
THEME_LAYOUT_DIR = "layout"
