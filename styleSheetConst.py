#Hex2Dec StyleSheet Constants

# \graphicImages --> directory containing all images needed for styleSheet

# ========== EXPLANATIONS ==========
# border-style --> defines border type: 4 parameters (4 sides)
#                                       3 parameters (top, left/right, bottom)
#                                       2 parameters (top/bottom, left/right)
#                                       1 parameter (all sides)
#
# color --> defines TEXT color inside element
# 
# COLORS: #1a1a1a (10% lightness in black), #ff3333 (60% lightness in red),
#        rgb(144,238,144) == lightgreen, rgb(173, 216, 230) == lightblue, rgb(128,128,128) == gray,
#       transparent (no text visible).
#
# margin --> space around object, padding --> space inside (border), outside (central element)
#
#


# ========== LABELS ==========

qLabelResultTitle_normal = """QLabel {
                                    color : #1a1a1a;
                                    font-size : 20px;
                                    border-style : solid;
                                    border-width : 1px;
                                    border-color : black;
                                    background-color : red;
                                    margin : 2px;
                               }""";
qLabelResultTitle_conversion = """QLabel {
                                         color : #1a1a1a;
                                         font-size : 20px;
                                         border-style : solid;
                                         border-width : 1px;
                                         border-color : black;
                                         background-color : white;
                                         margin : 2px;
                                   }""";
qLabelResultTitle_calculation = """QLabel {
                                          color : #1a1a1a;
                                          font-size : 20px;
                                          border-style : solid;
                                          border-width : 1px;
                                          border-color : black;
                                          background-color : yellow;
                                          margin : 2px;
                                   }""";
qLabelResultHex_normal = """QLabel {
                                   color : #1a1a1a;
                                   font-size : 12px;
                                   font-weight : bold;
                                   border-style : solid;
                                   border-width : 1px;
                                   border-color : green;
                                   background-color : lightgreen; 
                                   margin : 2px;
                            }""";

# During conversion/calculation of labelResultBin/Hex/Dec element, we want to show picture instead of text/background
# of the element. To achieve that, color (of text) must be: transparent, background-image becomes image from our directory.
# ** background-image : url(relativePath) --> named WITHOUT " ", possible version differences.

qLabelResultHex_conversion = """QLabel {
                                       color : transparent;
                                       border-style : solid;
                                       border-width : 1px;
                                       border-color : black;
                                       background-image : url(graphicImages\labelConversionImage.png); 
                                       margin : 1px;
                                }""";
qLabelResultHex_calculation = """QLabel {
                                        color : transparent;
                                        border-style : solid;
                                        border-width : 1px;
                                        border-color : black;
                                        background-image : url(graphicImages\labelCalculationImage.png); 
                                        margin : 1px;
                                 }""";
qLabelResultDec_normal = """QLabel {
                                   color : #1a1a1a;
                                   font-size : 12px;
                                   font-weight : bold;
                                   border-style : solid;
                                   border-width : 1px;
                                   border-color : blue;
                                   background-color : lightblue;
                                   margin : 2px;
                            }""";
qLabelResultDec_conversion = """QLabel {
                                       color : transparent;
                                       border-style : solid;
                                       border-width : 1px;
                                       border-color : black;
                                       background-image : url(graphicImages\labelConversionImage.png); 
                                       margin : 1px;
                                }""";
qLabelResultDec_calculation = """QLabel {
                                        color : transparent;
                                        border-style : solid;
                                        border-width : 1px;
                                        border-color : black;
                                        background-image : url(graphicImages\labelCalculationImage.png); 
                                        margin : 1px;
                                 }""";
qLabelResultBin_normal = """QLabel {
                                   color : #1a1a1a;
                                   font-size : 12px;
                                   font-weight : bold;
                                   border-style : solid;
                                   border-width : 1px;
                                   border-color : gray;
                                   background-color : lightgray;
                                   margin : 2px;
                            }""";
qLabelResultBin_conversion = """QLabel {
                                       color : transparent;
                                       border-style : solid;
                                       border-width : 1px;
                                       border-color : black;
                                       background-image : url(graphicImages\labelConversionImage.png); 
                                }""";
qLabelResultBin_calculation = """QLabel {
                                        color : transparent;
                                        border-style : solid;
                                        border-width : 1px;
                                        border-color : black;
                                        background-image : url(graphicImages\labelCalculationImage.png); 
                                        margin : 1px;
                                 }""";


# ========== BUTTONS ==========

qPushButtonConvert_all = """QPushButton {
                                        color : #1a1a1a;
                                        font-weight : bold;
                                        font-size : 20px;
                                        border-style : solid;
                                        border-width : 1px;
                                        border-radius : 14px;
                                        border-color : black;
                                        background-color : #ff3333;
                                        margin : 2px;
                            }
                            QPushButton:hover {
                                                border-width : 3px;
                                                margin : 1px;
                                                font-size : 25px;
                            }
                            QPushButton:pressed {
                                                 border-width : 3px;
                                                 margin : 5px;
                                                 font-size : 25px;
                            }
                            """;
qPushButtonCalculate_all = """QPushButton {
                                        color : #1a1a1a;
                                        font-weight : bold;
                                        font-size : 20px;
                                        border-style : solid;
                                        border-width : 1px;
                                        border-radius : 14px;
                                        border-color : black;
                                        background-color : #ff3333;
                                        margin : 2px;
                            }
                            QPushButton:hover {
                                                border-width : 3px;
                                                margin : 1px;
                                                font-size : 25px;
                            }
                            QPushButton:pressed {
                                                 border-width : 3px;
                                                 margin : 5px;
                                                 font-size : 25px;
                            }
                            """;


# ========== TEXT BOXES ==========

qTextBoxInput_all = """QTextEdit {
                                 color : #1a1a1a;
                                 border-style : solid;
                                 border-color : black;
                                 border-width : 2px;
                                 background-color : rgba(255,255,255,0.2);
                                 margin : 2px;
                         }
                         QTextEdit:hover {
                                         border-width : 4px;
                                         margin : 0px;
                         }""";


# ========== LINE BOXES ==========

qLineBoxOutputHex_normal = """QLineEdit {
                                        color : #1a1a1a;
                                        border-style : solid;
                                        border-color : green;
                                        border-width : 2px;
                                        background-color : rgba(144,238,144,0.3);
                                        margin : 2px;
                                        
                              }
                              QLineEdit:hover {
                                               border-width : 4px;
                                               margin : 0px;
                              }""";
qLineBoxOutputDec_normal = """QLineEdit {
                                        color : #1a1a1a;
                                        border-style : solid;
                                        border-color : blue;
                                        border-width : 2px;
                                        background-color : rgba(173,216,230,0.3);
                                        margin : 2px;
                              }
                              QLineEdit:hover {
                                               border-width : 4px;
                                               margin : 0px;
                              }""";
qLineBoxOutputBin_normal = """QLineEdit {
                                        color : #1a1a1a;
                                        border-style : solid;
                                        border-color : black;
                                        border-width : 2px;
                                        background-color : rgba(128,128,128,0.3);
                                        margin : 2px;
                              }
                              QLineEdit:hover {
                                            border-width : 4px;
                                            margin : 0px;
                              }""";
