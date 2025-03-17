import streamlit as st

answer = """
<think>
Okay, so I'm trying to figure out which articles from the provided context are violated when a government forbids peaceful assembly. Let me start by reading through each article carefully.

Looking at Article 20, it specifically mentions two points: 1) Everyone has the right to freedom of peaceful assembly and association, and 2) No one may be compelled to belong to an association. So if the government is forbidding assembly, that directly relates to point 1 here.

Wait, but what about other articles? For example, Article 30 talks about the United Nations' principles, which might not apply here since it's more about national rights. Article 22 is about social security and economic rights, so probably not relevant for this issue of assembly.

Then there's Article 19 regarding freedom of expression and opinion, but that doesn't seem to directly tie into forbidding assembly as much as Article 20 does. So I think the main violation here would be from Article 20, specifically point 1.
</think>

When a government forbids peaceful assembly, it violates Article 20 of the Declaration, which guarantees the right to freedom of assembly and association, ensuring no compulsion in such activities.
"""

think_content = answer.split("<think>")[1].split("</think>")[0].strip()
final_answer = answer.split("</think>")[1].strip()

think_content = '<div style="color: #6A6A6A; padding: 10px; border-radius: 5px;"><strong>Thought</strong><blockquote style="margin: 10px 0; border-left: 4px solid #6A6A6A; padding-left: 10px;">' + think_content + '</blockquote></div>'

# Display in chat
with st.chat_message("assistant"):
    st.markdown(think_content, unsafe_allow_html=True)