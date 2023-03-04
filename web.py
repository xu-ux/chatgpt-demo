import openai
import streamlit as st

api_key = "your key"
openai.api_key = api_key
message_list = []


def generate_response(message_list):
    """
    发送请求并获取响应
    :param message_list: 消息容器
    :return:
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # string | Only gpt-3.5-turbo and gpt-3.5-turbo-0301 are supported.
        messages=message_list,  # array | 要为其生成聊天完成的消息
        temperature=0.8,  # number | 情绪程度，介于 0 和 2 之间。较高的值（如 0.8）将使输出更加随机，而较低的值（如 0.2）将使其更加集中和确定
        # top_p = 1,        # number | 情绪程度的替代方法称为核心采样，0.1 -1 不要同时更改temperature和top_p
        # n = 1,            # number | 每个输入消息回复的聊天数目
        # max_tokens=4096,  # number |生成的答案允许的最大令牌数。默认情况下，模型可以返回的令牌数为4096
        stop='习近平',  # string or array | 最多 4 个序列，遇到这些词 API 将停止生成
    )
    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


st.title('ChatGPT Demo')
st.subheader("Model: gpt-3.5-turbo")
st.markdown('> [Api DOC](https://platform.openai.com/docs/api-reference/chat/create)')
st.markdown('> ')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input = st.text_area("You:", key='input')

if user_input:
    message_list.append({"role": "user", "content": user_input})
    output = generate_response(message_list)
    message_list.append({"role": "assistant", "content": output})
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

if st.session_state['generated']:
    for i in range(0, len(st.session_state['generated'])):
        st.markdown(f'''**You:** {st.session_state['past'][i]}''')
        st.markdown(f'''**AI:** {st.session_state["generated"][i]}''')


