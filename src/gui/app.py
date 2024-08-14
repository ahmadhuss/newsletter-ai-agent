import streamlit as st
import os
from newsletter_gen.crew import NewsletterGenCrew


class NewsletterGenUI:
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '..', 'newsletter_gen', 'config', 'newsletter_template.html')

    def load_html_template(self):
        with open(self.file_path, 'r') as file:
            html_template = file.read()
        return html_template  # read content and return as string

    # Newsletter Generator:
    def generate_newsletter(self, topic, personal_message):
        # Here will call the API of the Crew
        inputs = {
            'topic': topic,
            'personal_message': personal_message,
            'html_template': self.load_html_template()
        }
        return NewsletterGenCrew().crew().kickoff(inputs=inputs)

    # Newsletter Generator:
    def newsletter_generator(self):
        if st.session_state.generating:
            st.session_state.newsletter = self.generate_newsletter(
                st.session_state.topic, st.session_state.personal_message
            )
        # After newsletter generation we have to print
        if st.session_state.newsletter and st.session_state.newsletter != '':
            with st.container():
                st.write("News generated successfully!")
                # Convert the newsletter to a string if it isn't already
                if isinstance(st.session_state.newsletter, str):
                    html_content = st.session_state.newsletter
                else:
                    html_content = str(st.session_state.newsletter)

                st.download_button(
                    label="Download HTML file",
                    data=html_content,
                    file_name="news.html",
                    mime="text/html",
                )
            st.session_state.generating = False

    # Sidebar Component
    def sidebar(self):
        with st.sidebar:
            st.title('Gokiri News Generator via AI LLM Agents')
            st.write(
                'To generate a news, enter a topic and a personal message. \n Your team of AI agents will generate a news for you!')

            st.text_input("Topic", key="topic", placeholder="Singapore Weekly Press Release")

            st.text_area(
                "Your personal message (to include at the top of the news)",
                key="personal_message",
                placeholder="Personal Message",
            )

            if st.button('Generate News'):
                st.session_state.generating = True

    # Main render method
    def render(self):
        st.set_page_config(page_title='Gokiri AI Agents | Proof of concept', page_icon='📰')

        if 'topic' not in st.session_state:
            st.session_state.topic = ''

        if 'personal_message' not in st.session_state:
            st.session_state.personal_message = ''

        if 'newsletter' not in st.session_state:
            st.session_state.newsletter = ''

        if 'generating' not in st.session_state:
            st.session_state.generating = False

        self.sidebar()

        self.newsletter_generator()
        st.title('Gokiri AI Agents')


if __name__ == "__main__":
    NewsletterGenUI().render()
