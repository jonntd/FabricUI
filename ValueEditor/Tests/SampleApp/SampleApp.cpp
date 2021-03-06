// SampleApp.cpp : Defines the entry point for the console application.
//

#include "SampleApp.h"
#include <ViewItemFactory.h>
#include "SampleModel.h"

using namespace FabricUI::ValueEditor;

static QTime myTimer;
void SetStylesheet(const char* filename)
{
  QFile File(filename);
  File.open(QFile::ReadOnly);
  QString StyleSheet = QLatin1String(File.readAll());

  qApp->setStyleSheet(StyleSheet);
}

int main(int argc, char *argv[])
{
  QApplication a(argc, argv);
  SetStylesheet("styles.qss");

  // We create a FabricInstance in order to test
  FabricCore::Initialize();

  FabricCore::Client::CreateOptions createOptions;
  memset( &createOptions, 0, sizeof( createOptions ) );
  createOptions.guarded = true;

  FabricCore::Client client( NULL, NULL, &createOptions );

  FabricUI::ValueEditor::BaseModelItem* pSampleModel = BuildSampleModel( client );

  myTimer.start();
  MainWindow w;

  w.setModelItem( pSampleModel );

  // Now everything is connected up, try modifying a model value
  FabricUI::ValueEditor::BaseModelItem* pAModel = pSampleModel->GetChild(1);
  SampleModelItem* pFloatModel = dynamic_cast<SampleModelItem*>(pAModel);
  if (pFloatModel)
  {
    QVariant anotherValue(45.43f);
    pFloatModel->SetValueDirect(anotherValue);
  }
  w.show();
  return a.exec();
}

MainWindow::MainWindow()
{
  setCentralWidget( &m_treeWidget );

  bool var = connect(
    this, SIGNAL( modelChanged( FabricUI::ValueEditor::BaseModelItem* ) ),
    &m_treeWidget, SLOT( onSetModelItem( FabricUI::ValueEditor::BaseModelItem* ) )
    );

  printf( "%i", var );
}

void MainWindow::setModelItem( FabricUI::ValueEditor::BaseModelItem *model )
{
  emit modelChanged( model );
  //m_treeWidget.onSetModelItem( model );
}

#include "moc_SampleApp.cpp"
