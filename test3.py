from reports import DiagnosticsReportUlanUde2019, DiagnosticsReportChita2023

r = DiagnosticsReportChita2023(34891)
doc = r.create()
doc.save("test123.docx")