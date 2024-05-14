Option Explicit

Public Sub SaveInfomaxUnderlineIdentifier()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim retrieval_date As String
    Dim file_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("Derivatives")

    parameter_date = ws.Range("H2").Value
    retrieval_date = ws.Range("H3").Value
    file_name = ws.Range("H9").Value

    python_code = "import infomax_io;infomax_io.save_infomax_underline_identifier("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub