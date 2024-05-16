Option Explicit

Public Sub SaveInfomaxUnderlineIdentifier()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim retrieval_date As String
    Dim file_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("Derivatives")

    parameter_date = ws.Range("C2").Value
    retrieval_date = ws.Range("C3").Value
    file_name = ws.Range("C10").Value

    python_code = "import infomax_io;infomax_io.save_infomax_underline_identifier("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub LoadInfomaxUnderlineIdentifier()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim file_name As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "Derivatives"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C10").Value
    output_head = ws.Range("C14").Value

    python_code = "import infomax_io;infomax_io.load_infomax_underline_identifier("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "output_head = '" & output_head & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub