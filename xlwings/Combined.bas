Attribute VB_Name = "Combined"
Option Explicit

Public Sub SaveBbgTickersForDividend()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim deriva_und_file As String
    Dim index_weight_file As String
    Dim output_file As String
    Dim python_code As String

    ' Set the worksheet
    sheet_name = "Dividend"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C4").Value
    deriva_und_file = ws.Range("C13").Value
    index_weight_file = ws.Range("C12").Value
    output_file = ws.Range("C14").Value

    ' Set the python code
    python_code = "import combined_io;combined_io.save_bbg_tickers_for_dividend("
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "deriva_und_file='" & deriva_und_file & "',"
    python_code = python_code & "index_weight_file='" & index_weight_file & "',"
    python_code = python_code & "output_file='" & output_file & "')"

    ' Run the python code
    RunPython python_code
End Sub

    
    




    