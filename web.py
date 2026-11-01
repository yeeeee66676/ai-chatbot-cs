import streamlit as st

#设置页面配置项
import streamlit as st

st.set_page_config(
    page_title="Streamlit Demo",
    page_icon="😍",
    #布局
    layout="wide",
    #侧边栏状态
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://streamlit.io/',
        'Report a bug': "https://job.hust.edu.cn/searchJob.do?type=2&fbsj=",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

#官方streamlit文档
#大标题
st.title("入门演示")
st.header("一级标题")
st.subheader("二级标题")

#引入文字  st.write
st.write("111111111111111111111111111111")
st.write("222222222")
st.write("33333333333333333333333333333333")

#引入图片
st.image("./resourse/微信图片_20260723190707_4_18.jpg",width=200)
st.image("resourse/微信图片_20260723190707_4_18.jpg",width=200)

#引入音频 视频，同引入图片  st.audio st.video

#引入logo  st.logo

#引入表格  st.table
students={
    "姓名：":["张三","李四","王五"],
    "年龄：":[18,19,20],
    "性别：":["男","女","未知"]
}
st.table(students)

#输入框
name=st.text_input("请输入姓名")
st.write(f"{name}")
#密码输入框
name=st.text_input("请输入姓名",type="password")
st.write(f"{name}")

#单选按钮
st.radio("性别",["男","女"])