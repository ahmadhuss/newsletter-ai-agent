#!/usr/bin/env python
import os
from newsletter_gen.crew import NewsletterGenCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# Get the directory of the current script
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'config', 'newsletter_template.html')


def load_html_template():
    with open(file_path, 'r') as file:
        html_template = file.read()
    return html_template  # read content and return as string


# Input will be in the terminal for testing purpose
def run():
    inputs = {
        'topic': input('Enter the topic for your newsletter: '),
        'personal_message': input('Enter a personal message for your newsletter: '),
        'html_template': load_html_template()
    }

    # Calling our Class instance, that return the crew instance that run the kickoff
    NewsletterGenCrew().crew().kickoff(inputs=inputs)
