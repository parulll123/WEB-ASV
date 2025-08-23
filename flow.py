from graphviz import Digraph

# Create a Digraph
dot = Digraph(comment='Flowchart Kapal Otomatis AI + Fail-safe Remote')
dot.attr(rankdir='LR', size='10')

# Power Layer
dot.node('START', 'START', shape='ellipse', style='filled', color='lightgreen')
dot.node('BAT', 'Baterai', shape='parallelogram', style='filled', color='lightcoral')
dot.node('SW', 'Saklar: ON?', shape='diamond', style='filled', color='lightblue')
dot.node('PWR', 'Distribusi Daya', shape='box', style='filled', color='lightcyan')
dot.node('HP', 'Alur Daya Tinggi (ESC + Motor)', shape='box', style='filled', color='lightcyan')
dot.node('LP', 'Alur Daya Rendah (Raspberry Pi + Servo)', shape='box', style='filled', color='lightcyan')

# Control Layer
dot.node('INIT', 'Inisialisasi Sistem & Program', shape='box', style='filled', color='lightcyan')
dot.node('MODE', 'Pilih Mode Operasi', shape='diamond', style='filled', color='lightblue')
dot.node('AUTO', 'Mode Otomatis (OpenCV)', shape='box', style='filled', color='lightcyan')
dot.node('MANUAL', 'Mode Manual (Remote)', shape='box', style='filled', color='lightgrey')
dot.node('RUN_AI', 'Gerakkan ESC & Servo sesuai AI', shape='box', style='filled', color='lightcyan')
dot.node('COLLISION', 'Deteksi Tabrakan?', shape='diamond', style='filled', color='lightblue')
dot.node('FAILSAFE', 'Pindah ke Mode Manual', shape='box', style='filled', color='orange')
dot.node('RETURN', 'Kembali ke Start', shape='box', style='filled', color='lightgrey')

# Monitoring Layer
dot.node('WEB', 'Web Monitoring (Status, Posisi, Baterai)', shape='box', style='filled', color='lightyellow')

# Emergency Button
dot.node('EMG', 'Emergency Button?', shape='diamond', style='filled', color='lightblue')
dot.node('CUT', 'Putuskan Daya Motor & Servo', shape='box', style='filled', color='lightcoral')
dot.node('STOP', 'Sistem Mati', shape='box', style='filled', color='lightcyan')

# Connections
dot.edges([('START', 'BAT'), ('BAT', 'SW')])
dot.edge('SW', 'PWR', label='Yes', color='green')
dot.edge('SW', 'STOP', label='No', color='red')

dot.edge('PWR', 'HP')
dot.edge('PWR', 'LP')
dot.edge('HP', 'EMG')
dot.edge('LP', 'INIT')
dot.edge('INIT', 'MODE')
dot.edge('MODE', 'AUTO', label='Otomatis', color='green')
dot.edge('MODE', 'MANUAL', label='Manual', color='blue')

# AUTO mode path
dot.edge('AUTO', 'RUN_AI')
dot.edge('RUN_AI', 'COLLISION')
dot.edge('COLLISION', 'FAILSAFE', label='Yes', color='red')
dot.edge('FAILSAFE', 'MANUAL')
dot.edge('COLLISION', 'RUN_AI', label='No', color='green')

# MANUAL path
dot.edge('MANUAL', 'RETURN')
dot.edge('RETURN', 'START')

# Emergency button
dot.edge('EMG', 'CUT', label='Yes', color='red')
dot.edge('CUT', 'STOP')
dot.edge('EMG', 'RUN_AI', label='No', color='green')

# Monitoring
dot.edge('LP', 'WEB')
dot.edge('RUN_AI', 'WEB', style='dashed')
dot.edge('MANUAL', 'WEB', style='dashed')

# Save and render
output_path = r'C:/Users/Fahrul/Documents/ASV KAPAL/web/kapal_otomatis_flowchart'
dot.render(output_path, format='png', cleanup=False)

output_path + '.png'
