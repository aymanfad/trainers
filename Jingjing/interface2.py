import sys
from PyQt5 import QtWebEngineWidgets, QtCore, QtGui, QtWidgets
import pandas as pd
import networkx as nx
import folium
import matplotlib.pyplot as plt


class WelcomeWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.setWindowTitle("Welcome Window")

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QtWidgets.QLabel("Select Input Data File:")
        self.file_path_label = QtWidgets.QLabel()
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.file_path_label)
        vbox.addWidget(self.browse_button)

        self.central_widget.setLayout(vbox)

    def browse(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", "XLSX Files (*.xlsx)"
        )
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(self.file_path)
            self.hide()
            self.function_window = FunctionWindow(self.file_path)
            self.function_window.show()
            #self.function_window.show_complex_network_visualization(self.file_path)
            
class FunctionWindow(QtWidgets.QMainWindow):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Function Window")
        self.file_path = file_path

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QtWidgets.QLabel(f"File Path: {self.file_path}")
        self.spatial_temporal_analysis_button = QtWidgets.QPushButton("Spatial Temporal Analysis")
        self.network_resilience_analysis_button = QtWidgets.QPushButton("Network Resilience Analysis")
        self.model_uncertainty_button = QtWidgets.QPushButton("Model Uncertainty")
        self.shortest_path_analysis_button = QtWidgets.QPushButton("Shortest Path Analysis")
        self.complex_network_visualization_button = QtWidgets.QPushButton("Complex Network Visualization")
        self.complex_network_visualization_button.clicked.connect(self.show_complex_network_visualization)


        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.spatial_temporal_analysis_button)
        vbox.addWidget(self.network_resilience_analysis_button)
        vbox.addWidget(self.model_uncertainty_button)
        vbox.addWidget(self.shortest_path_analysis_button)
        vbox.addWidget(self.complex_network_visualization_button)
        

        self.central_widget.setLayout(vbox)
        
    def show_complex_network_visualization(self):
                df = pd.read_excel(self.file_path)
                G = nx.Graph()

                for st_id in df['st_id'].unique():
                    G.add_node(st_id)

                for i, row in df.iterrows():
                    if i > 0 and df['train'][i] == df['train'][i-1]:
                        G.add_edge(df['st_id'][i-1], df['st_id'][i])

                pos = {st_id: (df[df['st_id']==st_id]['lat'].iloc[0], df[df['st_id']==st_id]['lon'].iloc[0]) for st_id in G.nodes()}

                # Draw the network using networkx
                fig = plt.figure(figsize=(10, 8))
                nx.draw(G, pos=pos, with_labels=True)
                plt.axis('off')
                plt.show()

                # Create a folium map object
                m = folium.Map(location=[0, 0], zoom_start=2)

                # Add markers for each node in the network
                for st_id, (lat, lon) in pos.items():
                    folium.Marker([lat, lon], popup=str(st_id)).add_to(m)

                # Add edges to the map
                for u, v in G.edges():
                    folium.PolyLine([pos[u], pos[v]], color='gray', weight=1).add_to(m)
                    
                
                '''
                # Display the map in a new window
                map_window = MapWindow()
                map_window.setHtml(m._repr_html_())
                map_window.show()
                '''
                
                # Render the map as an HTML string
                html = m._repr_html_()
                
                # Create a new window to display the map
                self.map_window = MapWindow()
                self.map_window.set_html(html)

            
class MapWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Network Visualization")

        self.web_view = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.web_view)

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())