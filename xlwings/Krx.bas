Attribute VB_Name = "Krx"
Option Explicit

Public Sub SaveKrxEtfBase()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim file_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("BaseData")
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C5").Value

    python_code = "import krx_io;krx_io.save_krx_etf_base('" & parameter_date & "', '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxEtfPrice()
    Dim ws As Worksheet
    Dim retrieval_date As String
    Dim parameter_date As String
    Dim file_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("BaseData")
    retrieval_date = ws.Range("C3").Value
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C6").Value

    python_code = "import krx_io;krx_io.save_krx_etf_price("
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxStockPrice()
    Dim ws As Worksheet
    Dim retrieval_date As String
    Dim parameter_date As String
    Dim type_name As String
    Dim file_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("BaseData")
    retrieval_date = ws.Range("C3").Value
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C7").Value
    type_name = ws.Range("C8").Value

    python_code = "import krx_io;krx_io.save_krx_stock_price("
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "type_name = '" & type_name & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxEtfCombinedBase()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim base_file As String
    Dim price_file As String
    Dim output_file As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("BaseData")
    parameter_date = ws.Range("C4").Value
    base_file = ws.Range("C5").Value
    price_file = ws.Range("C6").Value
    output_file = ws.Range("C11").Value

    python_code = "import krx_io;krx_io.save_krx_etf_combined_base("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "base_file = '" & base_file & "',"
    python_code = python_code & "price_file = '" & price_file & "',"
    python_code = python_code & "output_file = '" & output_file & "')"

    RunPython python_code
End Sub


Public Sub LoadKrxEtfCombinedBase()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim file_name As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "BaseData"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C11").Value
    output_head = ws.Range("C12").Value

    ws.Range(output_head & "30:" & output_head & "2000").ClearContents

    python_code = "import krx_io;krx_io.load_krx_etf_combined_base("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxAll()
    Call SaveKrxEtfBase
    Call SaveKrxEtfPrice
    Call SaveKrxStockPrice
    Call SaveKrxIndexPrice
    Call SaveKrxEtfCombinedBase
    'Call SaveKrxEtfPdf
End Sub

Public Sub SaveKrxEtfPdf()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim etf_pdf_add_list_range As String
    Dim parameter_date As String
    Dim combined_base_file As String
    Dim pdf_file As String
    Dim min_cap As Double
    Dim market_type As String
    Dim sleep_time As Double
    Dim python_code As String

    sheet_name = "EtfPdf"
    etf_pdf_add_list_range = "EtfPdfAddList"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    
    parameter_date = ws.Range("C4").Value
    combined_base_file = ws.Range("C5").Value
    pdf_file = ws.Range("C6").Value
    min_cap = ws.Range("C7").Value
    market_type = ws.Range("C8").Value
    sleep_time = ws.Range("C9").Value

    python_code = "import krx_io;krx_io.save_krx_etf_pdf("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "etf_pdf_add_list_range = '" & etf_pdf_add_list_range & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "combined_base_file = '" & combined_base_file & "',"
    python_code = python_code & "pdf_file = '" & pdf_file & "',"
    python_code = python_code & "min_cap = " & min_cap & ","
    python_code = python_code & "market_type = '" & market_type & "',"
    python_code = python_code & "sleep_time = " & sleep_time & ")"

    RunPython python_code
End Sub

Public Sub LoadKrxEtfPdf()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim pdf_file As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "EtfPdf"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C4").Value
    pdf_file = ws.Range("C6").Value
    output_head = ws.Range("C10").Value

    ws.Range(output_head & "50:" & output_head & "20000").ClearContents

    python_code = "import krx_io;krx_io.load_krx_etf_pdf("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "pdf_file = '" & pdf_file & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxIndexPrice()
    Dim ws As Worksheet
    Dim retrieval_date As String
    Dim parameter_date As String
    Dim file_name As String
    Dim type_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("BaseData")
    retrieval_date = ws.Range("C3").Value
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C9").Value
    type_name = ws.Range("C10").Value

    python_code = "import krx_io;krx_io.save_krx_index_price("
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "type_name = '" & type_name & "')"

    RunPython python_code
End Sub

Public Sub LoadKrxIndexName()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim file_name As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "Index"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C5").Value
    output_head = ws.Range("C6").Value

    python_code = "import krx_io;krx_io.load_krx_index_name("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub
Public Sub SaveKrxDerivativesData()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim retrieval_date As String
    Dim end_date_cutoff As String
    Dim drop_spread As String
    Dim sleep_time As String
    Dim file_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("Derivatives")
    parameter_date = ws.Range("C2").Value
    retrieval_date = ws.Range("C3").Value
    end_date_cutoff = ws.Range("C4").Value
    sleep_time = ws.Range("C6").Value
    file_name = ws.Range("C7").Value

    If ws.Range("C5").Value = "Y" Then
        drop_spread = "True"
    Else
        drop_spread = "False"
    End If

    python_code = "import krx_io;krx_io.save_krx_derivatives_data("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "end_date_cutoff = '" & end_date_cutoff & "',"
    python_code = python_code & "drop_spread = " & drop_spread & ","
    python_code = python_code & "sleep_time = " & sleep_time & ","
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxKtbfUnderline()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim retrieval_date As String
    Dim file_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("Derivatives")
    parameter_date = ws.Range("C2").Value
    retrieval_date = ws.Range("C3").Value
    file_name = ws.Range("C8").Value

    python_code = "import krx_io;krx_io.save_krx_ktbf_underline("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxLastTradeTime()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim retrieval_date As String
    Dim file_name As String
    Dim python_code As String

    Set ws = ThisWorkbook.Sheets("Derivatives")
    parameter_date = ws.Range("C2").Value
    retrieval_date = ws.Range("C3").Value
    file_name = ws.Range("C9").Value

    python_code = "import krx_io;krx_io.save_krx_derivatives_last_trade_time("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub LoadKrxDerivativesData()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim file_name As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "Derivatives"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C7").Value
    output_head = ws.Range("C11").Value

    ws.Range(output_head & "30:" & output_head & "2000").ClearContents

    python_code = "import krx_io;krx_io.load_krx_derivatives_data("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub LoadKrxKtbfUnderline()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim file_name As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "Derivatives"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C8").Value
    output_head = ws.Range("C12").Value

    python_code = "import krx_io;krx_io.load_krx_ktbf_underline("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub LoadKrxDerivativesLastTime()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim file_name As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "Derivatives"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C9").Value
    output_head = ws.Range("C13").Value

    python_code = "import krx_io;krx_io.load_krx_derivatives_last_trade_time("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveAllDerivativesInfo()
    Call SaveKrxDerivativesData
    Call SaveKrxKtbfUnderline
    Call SaveKrxLastTradeTime
    Call InfomaxData.SaveInfomaxUnderlineIdentifier
End Sub


Public Sub LoadKrxEtfKtbfBondIsin()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim file_name As String
    Dim exclude_list As String
    Dim ktbf_und_file As String
    Dim output_head As String
    Dim python_code As String

    sheet_name = "BondMaster"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C3").Value
    exclude_list = ws.Range("C4").Value
    ktbf_und_file = ws.Range("C5").Value
    output_head = ws.Range("C6").Value

    python_code = "import krx_io;krx_io.load_krx_etf_ktbf_bond_isin("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "exclude_list = '" & exclude_list & "',"
    python_code = python_code & "ktbf_und_file = '" & ktbf_und_file & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveIndexShareFromETF()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim idx_etf_match_range_name As String
    Dim parameter_date As String
    Dim combined_etf_base_file As String
    Dim etf_pdf_file As String
    Dim output_file As String
    Dim python_code As String

    sheet_name = "Index"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    idx_etf_match_range_name = "IndexEtfMatch"
    parameter_date = ws.Range("C4").Value
    combined_etf_base_file = ws.Range("C7").Value
    etf_pdf_file = ws.Range("C8").Value
    output_file = ws.Range("C9").Value

    python_code = "import index_io;index_io.save_index_weight_from_etf("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "idx_etf_match_range_name = '" & idx_etf_match_range_name & "',"
    python_code = python_code & "combined_etf_base_file = '" & combined_etf_base_file & "',"
    python_code = python_code & "etf_pdf_file = '" & etf_pdf_file & "',"
    python_code = python_code & "output_file = '" & output_file & "')"

    RunPython python_code
End Sub
