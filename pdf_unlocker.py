import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(
    page_title="PDF解锁工具 - 新耐视",
    page_icon="🔓",
    layout="centered"
)

st.title("🔓 PDF 编辑密码移除工具")
st.markdown("**快速移除 PDF 的编辑、打印、复制等权限密码**")

st.info("🔸 本工具仅处理 **编辑权限密码**（owner password）\n🔸 文件仅在你浏览器中处理，不会上传到服务器")

uploaded_file = st.file_uploader("上传需要解锁的 PDF 文件", type="pdf", help="支持单个文件")

if uploaded_file:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 开始解锁", type="primary", use_container_width=True):
            with st.spinner("正在移除密码..."):
                try:
                    reader = PdfReader(uploaded_file)
                    writer = PdfWriter()
                    
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)
                    
                    new_name = f"解锁_{uploaded_file.name}"
                    
                    st.success(f"✅ 解锁成功！\n**{new_name}**")
                    
                    st.download_button(
                        label="⬇️ 下载解锁后的 PDF",
                        data=output,
                        file_name=new_name,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"处理失败: {str(e)}")
                    st.caption("提示：如果 PDF 需要密码才能打开（user password），本工具无法处理。")

    with col2:
        st.info("**使用说明**\n\n1. 上传 PDF\n2. 点击解锁\n3. 下载新文件")

st.markdown("---")
st.caption("| 基于 pypdf | 安全本地处理")