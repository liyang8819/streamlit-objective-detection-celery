import setuptools

setuptools.setup(
    name="streamlit-objective-detection-celery",
    version="0.1.1",
    author="YaNG Li",
    author_email="liyang.li@honeywell.com",
    description="Streamlit Image Annotation and objective detection model trainning with yolo5 and celery",
    long_description="It is a image annotation tool. You can use to do preprocessing of computer vision tasks and trainning yolo5 models.",
    long_description_content_type="text/plain",
    # url="https://github.com/lit26/streamlit-img-label",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires="==3.8.3",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
