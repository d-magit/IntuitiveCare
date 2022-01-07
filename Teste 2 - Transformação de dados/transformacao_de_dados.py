from tabula import read_pdf
options = ["-Dorg.slf4j.simpleLogger.defaultLogLevel=off", "-Dorg.apache.commons.logging.Log=org.apache.commons.logging.impl.NoOpLog"]
filename = 'padrao-tiss_componente-organizacional_202111.pdf' ## PDF file name

# Reading PDF
df = read_pdf(filename, pages=[114, 115, 116, 117, 118, 119, 120], encoding='utf-8', java_options=options)