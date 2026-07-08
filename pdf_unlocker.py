import streamlit as st
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError, FileNotDecryptedError, DependencyError
import io

st.set_page_config(
    page_title="PDF权限限制移除工具",
    layout="centered"
)

st.title("PDF 权限限制移除工具")
st.markdown("快速移除 PDF 的编辑、打印、复制等权限限制。")

st.warning(
    "请仅处理你本人拥有或已获得授权处理的 PDF 文件。\n\n"
    "说明：如果本工具部署在服务器或云端，文件会从浏览器上传到后端内存中处理；"
    "如果在你自己的电脑本地运行，则文件仅在本机后端内存中处理。"
)

uploaded_file = st.file_uploader(
    "上传需要处理的 PDF 文件",
    type=["pdf"],
    help="支持单个 PDF 文件",
    max_upload_size=100
)

if uploaded_file:
    file_bytes = uploaded_file.getvalue()

    # 简单校验 PDF 文件头，避免只靠扩展名判断
    if not file_bytes.startswith(b"%PDF"):
        st.error("文件格式不正确：这不是有效的 PDF 文件。")
        st.stop()

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("开始处理", type="primary", use_container_width=True):
            with st.spinner("正在处理 PDF..."):
                try:
                    input_pdf = io.BytesIO(file_bytes)
                    reader = PdfReader(input_pdf)

                    # 如果是权限型加密，通常空密码可以读取
                    if reader.is_encrypted:
                        decrypt_result = reader.decrypt("")

                        if decrypt_result == 0:
                            st.error("处理失败：该 PDF 需要打开密码，无法直接移除权限限制。")
                            st.stop()

                    # 尽量保留原 PDF 的结构、目录、元数据等
                    writer = PdfWriter(clone_from=reader)

                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)

                    new_name = f"unlocked_{uploaded_file.name}"

                    st.success(f"处理成功：{new_name}")

                    st.download_button(
                        label="下载处理后的 PDF",
                        data=output,
                        file_name=new_name,
                        mime="application/pdf",
                        use_container_width=True
                    )

                except DependencyError:
                    st.error(
                        "处理失败：该 PDF 可能使用 AES 加密，需要安装额外依赖：\n\n"
                        "pip install cryptography"
                    )

                except FileNotDecryptedError:
                    st.error("处理失败：该 PDF 需要打开密码，当前工具无法处理。")

                except PdfReadError:
                    st.error("处理失败：PDF 文件可能损坏、格式异常，或不是标准 PDF。")

                except Exception as e:
                    st.error(f"处理失败：{str(e)}")

    with col2:
        st.info(
            "使用说明\n\n"
            "1. 上传 PDF\n"
            "2. 点击开始处理\n"
            "3. 下载新文件\n\n"
            "限制说明：如果 PDF 需要输入打开密码，本工具无法处理。"
        )

st.markdown("---")
st.caption("基于 pypdf，仅用于授权文件的权限限制移除")