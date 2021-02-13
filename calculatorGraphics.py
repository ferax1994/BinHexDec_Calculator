#Dec-Bin-Hex calculator - GUI

# ==========
#   Date: 01.2021.
#
#   Imported non standard python packages: PyQt5 library for Python 3.5.x (outdated and unsupported).
#       pip install PyQt5
#
#   Updated and supported python packages: PySide6 library for Python 3.6.x and above.
#
#   Links for original documentation:
#       https://www.riverbankcomputing.com/static/Docs/PyQt5/
#
#   Links for updated documentation:
#       https://doc.qt.io/qtforpython/contents.html
#
# ==========

# ==========
#   Programer import guidelines:
#
#       from calculatorLogic import *;
#
#       Module calculatorLogic contains all calculation support uppon number/expression as string data.
#       Convert number with: data = Calculator().convert(numberString);
#
#
#       projectPath\graphicImages --> directory containing all images used to make graphic interface
#
# ==========

from PyQt5 import QtCore, QtGui;

from PyQt5.QtGui import QFont, QImage, QPalette, QBrush, QColor, QPainter, QIcon;
from PyQt5.QtCore import QSize, Qt, QRect, QEvent, QTimer;

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QMainWindow, QTextEdit, QLineEdit, QMessageBox, QAction, QFileDialog;  

import sys;
import time;
import styleSheetConst;

from calculatorLogic import *;

mainSize = (1000,700);
graphicChange_conversionTime = 500; #in miliseconds (ms)
graphicChange_calculationTime = 500; #in miliseconds (ms)

class Window(QMainWindow) :
    """Window class inherits QMainWindows functionality.
    All PyQt (visual) elements, are variables/features/childs of this class.
    All graphics elements functionality is implemented in this class (as an override or custom functions).
    Window class must be instanced in the same THREAD as QApplication to secure that all events will be part of the same process thread.

    Window class (through parent QMainWindow class) also inherits QObject functionality. Reimplementation of: eventFilter function, make this class also an
    eventFilterObject.
    

    Constructor arguments:
        None

    Slot variables:
        Public graphic:
            strongFont, weakFont, defaultFont : OFont objects. Fonts for other QObjects.
            pushConvertButton : QPushButton object. Defines convert button.
                                Used to convert Number string from INPUT FIELD to other bases.
                                Result shown at labels.
            pushCalculateButton : QPushButton object. Defines calculate button.
                                  Used to calculate Expression string from INPUT FIELD to number.
                                  Result shown at same input field and at labels.
            labelResultTitle : QLabel object. Label with text as title to mark result part of window.
            labelResultHex, labelResultBin, labelResultDec : QLabel objects. Labels with text to mark each result field individualy.
            lineBoxOutputHex, lineBoxOutputBin, lineBoxOutputDec : QLineEdit objects. Line edits for printing results.
            textBoxInput : QTextEdit object. Defines main INPUT FIELD of window.
                           Used for input of NUMBERS and EXPRESSIONS.
            timer1, timer2 : QTimer object. Used to raise timeout() signal, which is connected to functions
                             updating graphic elements to previous state.

        Public logic:
            calculator : Calculator object. Defines calculator and its functionalities. See module: calculatorLogic.
            
        Private:
            _image,_scaledImage,_transparentImage : QImage objects. QImage for custom Window background generation.
            _brush : QBrush object. QBrush for QPalette object consisting QImage object.
            _palette : QPalette object. QPalette for QMainWindow background.

    Other important local variables:
        openFileAction, saveAsAction, quitAction, undoInputAction, helpAction : QAction objects. Actions for MenuBar options.
        menuBar : QMenuBar object. MenuBar of Window.
        fileMenu, editMenu, helpMenu : QMenu objects. Connected with QActions objects.

    Defines initialization object functions:
        initBackground(self) : None. Generates background and elements needed.
        UiComponents(self) : None. Generates all visual elements of Window.

    Defines private object functions:
        _open_file(self) : None. Opens file open window for file input.
        _save_as(self) : None. Opens file save windows for file output.
        _close_application(self) : None. Closes application.
        _undo_input(self) : None. Undo input in INPUT FIELD.
        _clear_input(self) : None. Clear INPUT FIELD.
        _help_option(self) : None. Opens message box for help.
        _conversion_graphic(self) : None. Updates certain widgets during converion.
        _undo_conversion_graphic(self) : None. Reset updates on certain widgets after conversion/calculation.
        _calculation_graphic(self) : None. Updates certain widgets during calculation.
        
    Defines object functions:
        conversion_start(self) :
        calculation_start(self) :
        
    Defines static functions:
        setLineBoxFont(lineBox,textFont,fSize,textAlignment) : returns None. Sets font type/size, and text alignment of QLineEdit object.
        setTextBoxFont(textBox,textFont,fSize,textAlignment) : returns None. Sets font type/size, and text alignment of QTextEdit object.
        setImageOpacity(image, opacity) : returns new image as QImage object. Sets given opacity for the given image in form of new image.

    Handles exceptions:
        from calculatorLogic : InabilityToClearStringError : Exception. Handled during CALCULATION (pushButton) if there was no string from INPUT FIELD.
  
                
    """

    # ==========
    # INITIALIZATION :
    # ==========

    def __init__(self, parent=None) :
        super(Window, self).__init__(parent);
        self.setWindowTitle('Hex_Dec_Bin Converter');
        self.setWindowIcon(QIcon("mainWindowIcon.png"));
        self.setGeometry(100,100,mainSize[0],mainSize[1]);

        #DIGITRON :
        
        self.calculator = Calculator();


        #FILE MENU ACTIONS :
        
        openFileAction = QAction("&Open...", self);
        openFileAction.setShortcut("Ctrl+O");
        openFileAction.setStatusTip("Open file in input field");
        openFileAction.triggered.connect(self._open_file);
        
        saveAsAction = QAction("&Save As...", self);
        saveAsAction.setShortcut("Ctrl+Shift+S");
        saveAsAction.setStatusTip("Save input field");
        saveAsAction.triggered.connect(self._save_as);

        quitAction = QAction("&Quit", self);
        quitAction.setShortcut("Ctrl+Q");
        quitAction.setStatusTip("Leave the app...");
        quitAction.triggered.connect(self._close_application);


        #EDIT MENU ACTIONS :
        
        undoInputAction = QAction("&Undo input...", self);
        undoInputAction.setShortcut("Ctrl+Z");
        undoInputAction.setStatusTip("Undo change in input field");
        undoInputAction.triggered.connect(self._undo_input);

        clearInputAction = QAction("&Clear input...", self);
        clearInputAction.setShortcut("Ctrl+Shift+C");
        clearInputAction.setStatusTip("Clear input");
        clearInputAction.triggered.connect(self._clear_input);


        #HELP MENU ACTIONS :
        
        helpAction = QAction("&Help?", self);
        helpAction.setStatusTip("Helping...");
        helpAction.triggered.connect(self._help_option);

        
        #STATUS BAR SHOWN :
        
        self.statusBar();


        #MAIN MENU :
        
        mainMenu = self.menuBar();
        
        fileMenu = mainMenu.addMenu("&File");
        fileMenu.addAction(openFileAction);
        fileMenu.addAction(saveAsAction);
        fileMenu.addAction(quitAction);

        editMenu = mainMenu.addMenu("&Edit");
        editMenu.addAction(undoInputAction);
        editMenu.addAction(clearInputAction);

        helpMenu = mainMenu.addMenu("&Help");
        helpMenu.addAction(helpAction);
        
        
        #FONTS :
        
        self.strongFont = QFont('Impact');
        self.weakFont = QFont('Arial');
        self.defaultFont = QFont('Times New Roman', 12);


        #REST_OF_INITIALIZATION :
        
        self.initBackground();
        self.initTimers();
        self.UiComponents();

        self.show();
        
    def initBackground(self) :
        """Arguments: None

        Returns: None

        Used to generate background of the object (QMainWindow).
        """
        
        self._image = QImage('graphicImages/background.jpg');
        self._scaledImage = self._image.scaled(self.size(), Qt.IgnoreAspectRatio);

        self._transparentImage = self.setImageOpacity(self._scaledImage, 0.15);
        self._palette = QPalette();
        self._brush = QBrush(self._transparentImage);
        self._palette.setBrush(QPalette.Background, self._brush);
        
        self.setPalette(self._palette);

    def initTimers(self) :
        """Arguments: None

        Returns: None

        Used to initialize timers for graphic changes signals.
        """

        #Timer1 == Timer for graphic change on:
        #       self.labelResultTitle, self.labelResultBin, self.labelResultHex, self.labelResultDec
        # during conversion of input field.
        # ** SingleShot == count only once!
        
        self.timer1 = QTimer(self);
        self.timer1.setSingleShot(True);
        self.timer1.timeout.connect(self._undo_conversion_graphic);

        #Timer2 == Timer for graphic change during calculation.
        #   Using SAME _undo_conversion_graphic function, as the same graphic elements were changed.
        #   Initialized second timer for code clearnes purpose.
        self.timer2 = QTimer(self);
        self.timer2.setSingleShot(True);
        self.timer2.timeout.connect(self._undo_conversion_graphic);

        
    def UiComponents(self) :
        """Arguments: None

        Returns: None

        Used to initialize all GUI visual elements on Window.
        """
                          
        # ========== BUTTONS :
        
        self.pushConvertButton = QPushButton('C o n v e r t', self);
        self.pushConvertButton.setStyleSheet(styleSheetConst.qPushButtonConvert_all);
        self.pushConvertButton.setFont(self.strongFont);
                                        
        self.pushConvertButton.setGeometry(500,50,200,50);

        self.pushConvertButton.clicked.connect(self._conversion_graphic);
        self.pushConvertButton.clicked.connect(self.conversion_start);


        self.pushCalculateButton = QPushButton('C a l c u l a t e', self);
        self.pushCalculateButton.setStyleSheet(styleSheetConst.qPushButtonCalculate_all);
        self.pushCalculateButton.setFont(self.strongFont);

        self.pushCalculateButton.setGeometry(750,50,200,50);

        self.pushCalculateButton.clicked.connect(self._calculation_graphic);
        self.pushCalculateButton.clicked.connect(self.calculation_start);

        # ========== LABELS :
        
        self.labelResultTitle = QLabel('- - -  R E S U L T S  - - -', self);

        # labelResultTitle size:
        #       x = 200, y = 50
        self.labelResultTitle.setStyleSheet(styleSheetConst.qLabelResultTitle_normal);
        self.labelResultTitle.setGeometry(100,550,200,50);
        self.labelResultTitle.setAlignment(Qt.AlignCenter);
        self.labelResultTitle.setFont(self.strongFont);

        
        self.labelResultHex = QLabel('Hex: ', self);
        self.labelResultDec = QLabel('Dec: ', self);
        self.labelResultBin = QLabel('Bin: ', self);

        # labelResultBin/Hex/Dec size:
        #       x = 100, y = 40
        self.labelResultHex.setGeometry(100,650,100,40);
        self.labelResultDec.setGeometry(600,650,100,40);
        self.labelResultBin.setGeometry(100,700,100,40);
        
        self.labelResultHex.setAlignment(Qt.AlignCenter);
        self.labelResultDec.setAlignment(Qt.AlignCenter);
        self.labelResultBin.setAlignment(Qt.AlignCenter);
        
        self.labelResultHex.setStyleSheet(styleSheetConst.qLabelResultHex_normal);
        self.labelResultDec.setStyleSheet(styleSheetConst.qLabelResultDec_normal);
        self.labelResultBin.setStyleSheet(styleSheetConst.qLabelResultBin_normal);
        
        self.labelResultHex.setFont(self.weakFont);
        self.labelResultDec.setFont(self.weakFont);
        self.labelResultBin.setFont(self.weakFont);


        # ========== TEXTEDIT :
        
        self.textBoxInput = QTextEdit(self);
        self.textBoxInput.setGeometry(10,50,450,150);
        self.textBoxInput.setStyleSheet(styleSheetConst.qTextBoxInput_all);
        
        self.setTextBoxFont(self.textBoxInput, 'Bookman Old Style', 14, Qt.AlignRight);

        self.textBoxInput.installEventFilter(self);


        # ========== LINEEDIT :
        
        self.lineBoxOutputHex = QLineEdit('0xFF', self);
        self.lineBoxOutputDec = QLineEdit('255', self);
        self.lineBoxOutputBin = QLineEdit('0b11111111', self);

        self.lineBoxOutputHex.setGeometry(220,650,250,40);
        self.lineBoxOutputDec.setGeometry(720,650,250,40);
        self.lineBoxOutputBin.setGeometry(220,700,250,40);
        
        self.lineBoxOutputHex.setAlignment(Qt.AlignCenter);
        self.lineBoxOutputDec.setAlignment(Qt.AlignCenter);
        self.lineBoxOutputBin.setAlignment(Qt.AlignCenter);
        
        self.lineBoxOutputHex.setStyleSheet(styleSheetConst.qLineBoxOutputHex_normal);
        self.lineBoxOutputDec.setStyleSheet(styleSheetConst.qLineBoxOutputDec_normal);
        self.lineBoxOutputBin.setStyleSheet(styleSheetConst.qLineBoxOutputBin_normal);
        
        self.setLineBoxFont(self.lineBoxOutputHex, 'Bookman Old Style', 13, Qt.AlignCenter);
        self.setLineBoxFont(self.lineBoxOutputDec, 'Bookman Old Style', 13, Qt.AlignCenter);
        self.setLineBoxFont(self.lineBoxOutputBin, 'Bookman Old Style', 13, Qt.AlignCenter);


    # ==========
    # MENU FUNCTIONS:
    # ==========
    
    def _open_file(self) :
        """Arguments: None

        Returns: None

        Used to open (text) files to be imported into input field of application.
        Generates QFileDialog window for file open.
        """

        #Look in: _save_as function, for QFileDialog disambugation.
        
        fileNameTuple = QFileDialog.getOpenFileName(self, "Open File", filter="Text (*.txt);;Python (*.py);;All files (*)");
        fileName = fileNameTuple[0];

        try :
            file = open(fileName, 'r');
            text = file.read();
            self.textBoxInput.setPlainText(text);
            file.close();
        except :
            pass;
    def _save_as(self) :
        """Arguments: None

        Returns: None

        Used to save (text) from input field of application to file.
        Generates QFileDialog window for file save.
        """

        #QFileDialog can be created through static functions :
        #   fileNameTuple = QFileDialog.getSaveFileName(parent=self, FileDialogName="Save As") <----
        #   fileName = fileNameTuple[0]
        #   ** in this version of PyQt5 QFileDialog.getSaveFileName() returns string tuple
        #   ** filter="Name (*.extension);;NextName (*.nextExtension)"

        #QFileDialog object can be created explicitly, to change more options.
        #   In that case, created instance of QFileDialog, as being external part of QMainWindow,
        #   must be executed using python .exec_() function.
        #   if (fileDialog.exec_() == QtWidgets.QDialog.Accepted) :
        #       do something

        fileNameTuple = QFileDialog.getSaveFileName(self, "Save As", filter="Text (*.txt);;Python (*.py);;All files (*)");
        fileName = fileNameTuple[0];
        try :
            file = open(fileName, 'w');
            text = self.textBoxInput.toPlainText();
            file.write(text);
            file.close();
        except :
            #all kinds of errors, mostly non existing fileName
            pass;

    def _close_application(self) :
        """Arguments: None

        Returns: None

        Used to close application from one more place (MenuBar-->FileMenu-->Quit).
        Generates QMessageBox window for user confirmation.
        """

        #QMessageBox can be created through static functions :
        #   question = QMessageBox.question(parent=self, MessageBoxName="Quit PopUp", MessageBoxText="Are you sure?",
        #                                       MessageBoxStandardButtons(Yes|No))

        #QMessageBox object can be created explicitly, to change more options.
        #   In that case, created instance of QMessageBox, as being external part ofQMainWindow,
        #   must be executed using python .exec_() function.
        #   var = messageBox.exec_()
        
        closePop = QMessageBox.question(self, "Quit PopUp",
                                       "Are you sure?",
                                       QMessageBox.Yes | QMessageBox.No);

        if (closePop == QMessageBox.Yes) :
            sys.exit();
        else :
            pass;

    def _undo_input(self) :
        """Arguments: None

        Returns: None

        Used to undo input field change through QTextEdit function: undo().
        """
        
        self.textBoxInput.undo();

    def _clear_input(self) :
        """Arguments: None

        Returns: None

        Used to clear input field through QTextEdit function: setPlainText("").
        Updates font and alignment of input field.
        """
        
        self.textBoxInput.setPlainText("");
        self.setTextBoxFont(self.textBoxInput, 'Bookman Old Style', 14, Qt.AlignRight);

    def _help_option(self) :
        """Arguments: None

        Returns: None

        Used to generate help dialog.
        Generates QMessageBox window for user choice.
        """

        #Look in: _close_application function, for QMessageBox disambugation
        
        helpPop = QMessageBox(self);
        helpPop.setWindowTitle("Help is here");
        helpPop.setWindowIcon(QIcon("graphicImages/helpIcon.png"));
        helpPop.setIcon(QMessageBox.Warning);
        helpPop.setText("We suggest reading source code and its comments");
        helpPop.setInformativeText("Help mail: ferax22@outlook.com");
        helpPop.setStandardButtons(QMessageBox.Ok | QMessageBox.Ignore | QMessageBox.Cancel);
        helpPop.setDefaultButton(QMessageBox.Cancel);
        helpPop.setDetailedText("Details...");
        #helpPop.buttonClicked.connect(lambda: [self.textBoxInput.setPlainText("Help"), self.textBoxInput.setAlignment(Qt.AlignRight)]);
        returnValue = helpPop.exec_();
        if (returnValue == QMessageBox.Ok) :
            self.textBoxInput.setText("Help served");
            self.textBoxInput.setAlignment(Qt.AlignRight);
        else :
            pass;

    # ==========
    # BUTTON GRAPHICAL FUNCTIONS:
    # ==========

    def _conversion_graphic(self) :
        """Arguments: None

        Returns: None

        During conversion (pushConvertButton.clicked()), changes display of some graphical elements using style sheets.
        """
        
        self.labelResultTitle.setStyleSheet(styleSheetConst.qLabelResultTitle_conversion);
        self.labelResultTitle.update();

        self.labelResultHex.setStyleSheet(styleSheetConst.qLabelResultHex_conversion);
        self.labelResultHex.update();
        self.labelResultDec.setStyleSheet(styleSheetConst.qLabelResultDec_conversion);
        self.labelResultDec.update();
        self.labelResultBin.setStyleSheet(styleSheetConst.qLabelResultBin_conversion);
        self.labelResultBin.update();

        self.timer1.start(graphicChange_conversionTime);

    def _undo_conversion_graphic(self) :
        """Arguments: None

        Returns: None

        Undo (Resets) graphic changes to elements affected in: _conversion_graphic() and _calculation_graphic functions().
        """

        self.labelResultTitle.setStyleSheet(styleSheetConst.qLabelResultTitle_normal);
        self.labelResultTitle.update();

        self.labelResultHex.setStyleSheet(styleSheetConst.qLabelResultHex_normal);
        self.labelResultHex.update();
        self.labelResultDec.setStyleSheet(styleSheetConst.qLabelResultDec_normal);
        self.labelResultDec.update();
        self.labelResultBin.setStyleSheet(styleSheetConst.qLabelResultBin_normal);
        self.labelResultBin.update();
        

    def _calculation_graphic(self) :
        """Arguments: None

        Returns: None

        During calculation (pushCalculateButton.clicked()), changes display of some graphical elements using style sheets.
        """
        
        self.labelResultTitle.setStyleSheet(styleSheetConst.qLabelResultTitle_calculation);
        self.labelResultTitle.update();

        self.labelResultHex.setStyleSheet(styleSheetConst.qLabelResultHex_calculation);
        self.labelResultHex.update();
        self.labelResultDec.setStyleSheet(styleSheetConst.qLabelResultDec_calculation);
        self.labelResultDec.update();
        self.labelResultBin.setStyleSheet(styleSheetConst.qLabelResultBin_calculation);
        self.labelResultBin.update();

        self.timer2.start(graphicChange_calculationTime);
        

    # ==========
    # BUTTON TASK_TO_DO FUNCTIONS:
    # ==========
        

    def conversion_start(self) :
        strNum = self.textBoxInput.toPlainText();
        self.setTextBoxFont(self.textBoxInput, 'Bookman Old Style', 13, Qt.AlignRight);
        try :
            resultTuple = self.calculator.convert(strNum);
            self.lineBoxOutputBin.setText(resultTuple[0]);
            self.lineBoxOutputHex.setText(resultTuple[1]);
            self.lineBoxOutputDec.setText(resultTuple[2]);
            self._clear_input();
        except TypeError as tEr :
            self.textBoxInput.setPlainText(str(tEr));
            self.lineBoxOutputBin.setText("NaN");
            self.lineBoxOutputHex.setText("NaN");
            self.lineBoxOutputDec.setText("NaN");
        except InabilityToAsignError as inErr :
            self.textBoxInput.setPlainText(str(inErr));
            self.lineBoxOutputBin.setText("NaN");
            self.lineBoxOutputHex.setText("NaN");
            self.lineBoxOutputDec.setText("NaN");
        except Exception as err :
            self.textBoxInput.setPlainText(str(err));
            self.lineBoxOutputBin.setText("----------");
            self.lineBoxOutputHex.setText("----------");
            self.lineBoxOutputDec.setText("----------");
        
        

    def calculation_start(self) :
        expStr = self.textBoxInput.toPlainText();
        try :
            expStr = self.calculator.stringClearStrip(expStr);
        except InabilityToClearStringError as incE :
            print("Window.calculation_start --> " + str(incE));
        except :
            print("Window.calculation_start --> unknown!");

        self.setTextBoxFont(self.textBoxInput, 'Times New Roman', 10, Qt.AlignLeft);
        
        
        self.textBoxInput.setPlainText("=== "+ expStr + " ---> " + str(Calculator.is_exp(expStr)));

    # ==========
    # EVENT HANDLING:
    # ==========

    def eventFilter(self, obj, event) :
        """Arguments:
                obj : QWidget/QObject. Part of Window.
                event : QEvent. Event uppon tasks are done.

        Returns:
            True/False : bool. True - further events blocked, False - further events permitted.
            **super().eventFilter(*args) : bool. Same behaviour. 
        

        EventFilter function reimplements function of the same name from QObject base class.
        Window class is EventFilterObject for other Widgets, and reimplementing ths function is mandatory.
        All QtCore events at Window, are filtered through this function.
        """
        
##        #MOUSE_POSITION_AND_CLICK
##        if (event.type() == QEvent.MouseButtonPress) :
##            if (event.button() == Qt.LeftButton) :
##                mousePos = event.pos();
##                #self._isClickOnWidget(mousePos);
                
        #TEXTEDIT
        if ((event.type() == QEvent.KeyPress) and (obj is self.textBoxInput)) :
            if ((event.key() == Qt.Key_Return) and self.textBoxInput.hasFocus()) :
                self.pushCalculateButton.animateClick();
                print("textInputBox-Enter");
                
        return False;
        

##    def _isClickOnWidget(self, pos) :
##        for attr,value in self.__dict__.items() :
##            if (self.attr.isWidgetType()) :
##                print(attr);
##                (w, h) = (self.attr.size().width(), self.attr.size().height());
##                print(w, h);

        


    # ==========
    # STATIC FUNCTIONS:
    # ==========
    
    @staticmethod
    def setLineBoxFont(lineBox, textFont, fSize, textAlignment) :
        """Arguments:
                lineBox : QLineEdit object uppon font change is set.
                textFont : String. Proper font name needed.
                fSize : int. Font size.
                textAlignment : Qt CONST.
            
        Returns: None

        If invalid parameters are passed, function will set: font and alignment, to default.
        """
        
        try :
            lineBox.setFont(QFont(textFont, fSize));
            lineBox.setAlignment(textAlignment);
        except :
            #catches various excepts
            lineBox.setFont(self.defaultFont);
            lineBox.setAlignment(Qt.AlignCenter);
                          
    @staticmethod
    def setTextBoxFont(textBox, textFont, fSize, textAlignment) :
        """Arguments:
                textBox : QTextEdit object uppon font change is set.
                textFont : String. Proper font name needed.
                fSize : int. Font size.
                textAlignment : Qt CONST.
                
        Returns: None

        If invalid parameters are passed, function will set: font and alignment, to default.
        """
        
        try :
            textBox.setFont(QFont(textFont, fSize));
            textBox.setAlignment(textAlignment);
        except :
            #catches various excepts
            textBox.setFont(self.defaultFont);
            textBox.setAlignment(Qt.AlignCenter);
        
    @staticmethod
    def setImageOpacity(image, opacity) :
        """Arguments:
                image : QImage object uppon opacity effect is performed.
                opacity : Float. Number from interval [0,1]. Any number: >1, is considered as: 1, by default.

        Returns:
            newImage : QImage object with new opacity feature.

        Does:
            1) NewImage is instantly created with dimensions of: image. It is filled with white color (non transparent).
            2) QPainter object: painter, is created with: newImage as argument. It accepts: opacity feature!
            3) Painter draws the same function argument: image, on: newImage.
        """
        
        newImage = QImage(image.size(), QImage.Format_ARGB32);
        newImage.fill(QColor(255,255,255,255));
        painter = QPainter(newImage);
        painter.setOpacity(opacity);
        painter.drawImage(QRect(0,0,image.width(),image.height()), image);
        return newImage;


##class TextBoxInput(QTextEdit) :
##    def __init__(self, parent) :
##        super().__init__(parent);
##
##    def keyPressEvent(self,event) :
##        if (event.key() == QtCore.QtKey_Return) :
##            self.setDisabled(True);
##            print("Enter works");
##
##        return super(TextBoxInput, self).keyPressEvent(event);

            
        
if (__name__== '__main__') :
    app = QApplication(sys.argv);
    window = Window();
    sys.exit(app.exec_());
