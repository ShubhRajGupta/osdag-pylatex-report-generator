import os
import pandas as pd
from datetime import datetime


class BeamReportGenerator:
    """
    A class to generate professional PDF engineering reports for beam analysis.
    
    """
    
    def __init__(self, excel_path: str, beam_image_path: str, output_name: str = "Beam_Analysis_Report"):
        """
        Initialize the BeamReportGenerator.
        
        Args:
            excel_path: Path to the Excel file with force data
            beam_image_path: Path to the beam diagram image
            output_name: Output PDF filename (default: Beam_Analysis_Report)
        """
        self.excel_path = excel_path
        self.beam_image_path = beam_image_path
        self.output_name = output_name
        self.data = None
        self.beam_length = 0
        
    def load_data(self) -> None:
        """
        Load and process data from the Excel file.

        """
        print("[INFO] Loading data from Excel file...")
        self.data = pd.read_excel(self.excel_path)
        
        # Calculate beam length from the maximum x value
        self.beam_length = self.data['x'].max()
        
        print(f"[INFO] Loaded {len(self.data)} data points")
        print(f"[INFO] Beam length: {self.beam_length} m")
        
    def _create_preamble(self) -> str:
        """
        Create the LaTeX document preamble with all required packages.
        
        Returns:
            String containing the LaTeX preamble
        """
        preamble = r"""
\documentclass[12pt, a4paper]{report}

% ============================================
% PACKAGES
% ============================================
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{float}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{tocloft}

% ============================================
% PAGE SETUP
% ============================================
\geometry{
    left=25mm,
    right=25mm,
    top=25mm,
    bottom=25mm
}

% ============================================
% PGFPLOTS CONFIGURATION
% ============================================
\pgfplotsset{compat=1.18}

% ============================================
% COLOR DEFINITIONS
% ============================================
\definecolor{shearpositive}{RGB}{70, 130, 180}    % Steel Blue
\definecolor{shearnegative}{RGB}{220, 20, 60}     % Crimson Red
\definecolor{momentpositive}{RGB}{34, 139, 34}    % Forest Green
\definecolor{momentnegative}{RGB}{255, 140, 0}    % Dark Orange
\definecolor{titleblue}{RGB}{0, 51, 102}          % Dark Blue

% ============================================
% HYPERREF SETUP
% ============================================
\hypersetup{
    colorlinks=true,
    linkcolor=titleblue,
    filecolor=magenta,      
    urlcolor=cyan,
    pdftitle={Beam Analysis Report},
    pdfauthor={FOSSEE Project},
}

% ============================================
% HEADER AND FOOTER
% ============================================
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Beam Analysis Report}
\fancyhead[R]{\small \leftmark}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% ============================================
% TITLE FORMATTING
% ============================================
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries\color{titleblue}}
  {\chaptertitlename\ \thechapter}{20pt}{\Huge}

\begin{document}
"""
        return preamble
    
    def _create_title_page(self) -> str:
        """
        Create a professional title page for the report.
        
        Returns:
            String containing LaTeX code for the title page
        """
        current_date = datetime.now().strftime("%B %d, %Y")
        
        title_page = r"""
% ============================================
% TITLE PAGE
% ============================================
\begin{titlepage}
    \centering
    
    \vspace*{2cm}
    
    % Title
    {\Huge\bfseries\color{titleblue} Structural Analysis Report \par}
    
    \vspace{1cm}
    
    {\LARGE\bfseries Simply Supported Beam Analysis \par}
    
    \vspace{2cm}
    
    % Decorative line
    \noindent\rule{\textwidth}{2pt}
    
    \vspace{2cm}
    
    % Project Information
    {\Large\textbf{Project:} FOSSEE Beam Analysis \par}
    
    \vspace{0.5cm}
    
    {\Large\textbf{Document Type:} Engineering Analysis Report \par}
    
    \vspace{0.5cm}
    
    {\Large\textbf{Analysis Method:} Shear Force \& Bending Moment Analysis \par}
    
    \vspace{3cm}
    
    % Date
    {\large\textbf{Date:} """ + current_date + r""" \par}
    
    \vfill
    
    % Footer line
    \noindent\rule{\textwidth}{1pt}
    
    \vspace{0.5cm}
    
    {\small Generated using Python and \LaTeX{} \par}
    
\end{titlepage}
"""
        return title_page
    
    def _create_toc(self) -> str:
        """
        Create the table of contents.
        
        Returns:
            String containing LaTeX code for the TOC
        """
        toc = r"""
% ============================================
% TABLE OF CONTENTS
% ============================================
\tableofcontents
\thispagestyle{empty}
\newpage
"""
        return toc
    
    def _create_introduction(self) -> str:
        """
        Create the introduction section with the beam diagram.
        
        Returns:
            String containing LaTeX code for the introduction
        """
        # Convert Windows path to forward slashes for LaTeX
        image_path = self.beam_image_path.replace("\\", "/")
        
        introduction = r"""
% ============================================
% INTRODUCTION
% ============================================
\chapter{Introduction}

\section{Overview}

This report presents a comprehensive structural analysis of a simply supported beam 
subjected to a uniformly distributed load. The analysis includes the calculation and 
visualization of internal forces, specifically the Shear Force Diagram (SFD) and 
Bending Moment Diagram (BMD).

\section{Simply Supported Beam}

A simply supported beam is a fundamental structural element that rests on two 
supports --- a pinned support at one end and a roller support at the other. This 
configuration allows the beam to:

\begin{itemize}
    \item Resist vertical loads through reaction forces at the supports
    \item Freely expand or contract due to thermal effects (roller support)
    \item Rotate freely at both support points
\end{itemize}

\subsection{Beam Configuration}

The beam under analysis has the following configuration:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{""" + image_path + r"""}
    \caption{Simply Supported Beam with Pinned and Roller Supports}
    \label{fig:beam_diagram}
\end{figure}

\textbf{Beam Parameters:}
\begin{itemize}
    \item \textbf{Total Length:} """ + f"{self.beam_length:.1f}" + r""" meters
    \item \textbf{Left Support:} Pinned support (restricts horizontal and vertical displacement)
    \item \textbf{Right Support:} Roller support (restricts only vertical displacement)
    \item \textbf{Loading:} Uniformly distributed load
\end{itemize}

\section{Analysis Objectives}

The objectives of this structural analysis are:

\begin{enumerate}
    \item Calculate shear forces at critical points along the beam
    \item Calculate bending moments at critical points along the beam
    \item Generate Shear Force Diagram (SFD)
    \item Generate Bending Moment Diagram (BMD)
    \item Identify maximum shear force and bending moment locations
\end{enumerate}

\newpage
"""
        return introduction
    
    def _create_data_table(self) -> str:
        """
        Create the input data table as a LaTeX tabular.
        
        This creates a professional table with selectable text,
        not an embedded image.
        
        Returns:
            String containing LaTeX code for the data table
        """
        # Start the chapter and table
        table_section = r"""
% ============================================
% INPUT DATA
% ============================================
\chapter{Input Data}

\section{Force and Moment Data}

The following table presents the calculated values of shear force and bending 
moment at various positions along the beam. These values were obtained from 
structural analysis calculations.

\begin{table}[H]
    \centering
    \caption{Shear Force and Bending Moment Values Along the Beam}
    \label{tab:force_data}
    \vspace{0.5cm}
    \begin{tabular}{|c|c|c|}
        \hline
        \rowcolor{titleblue!20}
        \textbf{Position (x)} & \textbf{Shear Force (V)} & \textbf{Bending Moment (M)} \\
        \textbf{[meters]} & \textbf{[kN]} & \textbf{[kN$\cdot$m]} \\
        \hline
"""
        
        # Add data rows from the DataFrame
        for idx, row in self.data.iterrows():
            x_val = row['x']
            shear = row['Shear force']
            moment = row['Bending Moment']
            
            # Format the row with proper alignment
            table_section += f"        {x_val:.1f} & {shear:.2f} & {moment:.2f} \\\\\n"
            table_section += "        \\hline\n"
        
        # Close the table
        table_section += r"""    \end{tabular}
\end{table}

\section{Data Interpretation}

From the table above, we can observe:

\begin{itemize}
    \item \textbf{Maximum Positive Shear Force:} """ + f"{self.data['Shear force'].max():.2f}" + r""" kN (at x = """ + f"{self.data.loc[self.data['Shear force'].idxmax(), 'x']:.1f}" + r""" m)
    \item \textbf{Maximum Negative Shear Force:} """ + f"{self.data['Shear force'].min():.2f}" + r""" kN (at x = """ + f"{self.data.loc[self.data['Shear force'].idxmin(), 'x']:.1f}" + r""" m)
    \item \textbf{Maximum Bending Moment:} """ + f"{self.data['Bending Moment'].max():.2f}" + r""" kN$\cdot$m (at x = """ + f"{self.data.loc[self.data['Bending Moment'].idxmax(), 'x']:.1f}" + r""" m)
    \item \textbf{Zero Shear Location:} x = """ + f"{self.data.loc[self.data['Shear force'] == 0, 'x'].values[0] if 0 in self.data['Shear force'].values else 'N/A'}" + r""" m (point of maximum moment)
\end{itemize}

\newpage
"""
        return table_section
    
    def _create_sfd_diagram(self) -> str:
        """
        Create the Shear Force Diagram using TikZ/pgfplots.
        
        Creates a professional bar chart with positive values in blue
        and negative values in red.
        
        Returns:
            String containing LaTeX code for the SFD
        """
        # Prepare data for positive and negative bars
        positive_coords = ""
        negative_coords = ""
        
        for idx, row in self.data.iterrows():
            x_val = row['x']
            shear = row['Shear force']
            
            if shear >= 0:
                positive_coords += f"            ({x_val}, {shear})\n"
                negative_coords += f"            ({x_val}, 0)\n"
            else:
                positive_coords += f"            ({x_val}, 0)\n"
                negative_coords += f"            ({x_val}, {shear})\n"
        
        sfd_section = r"""
% ============================================
% SHEAR FORCE DIAGRAM
% ============================================
\chapter{Analysis Results}

\section{Shear Force Diagram (SFD)}

The Shear Force Diagram shows the variation of internal shear force along the 
length of the beam. Positive shear forces are shown in \textcolor{shearpositive}{\textbf{blue}} 
and negative shear forces are shown in \textcolor{shearnegative}{\textbf{red}}.

\begin{figure}[H]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            width=0.95\textwidth,
            height=8cm,
            xlabel={Position along beam (m)},
            ylabel={Shear Force (kN)},
            title={\textbf{Shear Force Diagram}},
            xmin=-0.5,
            xmax=""" + f"{self.beam_length + 0.5}" + r""",
            ymin=""" + f"{self.data['Shear force'].min() - 10}" + r""",
            ymax=""" + f"{self.data['Shear force'].max() + 10}" + r""",
            xtick={""" + ",".join([str(x) for x in self.data['x']]) + r"""},
            grid=both,
            grid style={line width=0.2pt, draw=gray!30},
            major grid style={line width=0.4pt, draw=gray!50},
            axis lines=middle,
            axis line style={->, thick},
            legend style={
                at={(0.98,0.98)},
                anchor=north east,
                draw=black,
                fill=white,
                font=\small
            },
            every axis plot/.append style={thick},
            ybar,
            bar width=8pt,
            enlarge x limits=0.05,
        ]
        
        % Positive Shear Force (Blue)
        \addplot[
            fill=shearpositive,
            draw=shearpositive!80!black,
        ] coordinates {
""" + positive_coords + r"""        };
        \addlegendentry{Positive Shear}
        
        % Negative Shear Force (Red)
        \addplot[
            fill=shearnegative,
            draw=shearnegative!80!black,
        ] coordinates {
""" + negative_coords + r"""        };
        \addlegendentry{Negative Shear}
        
        % Zero line
        \draw[black, thick, dashed] (axis cs:-0.5,0) -- (axis cs:""" + f"{self.beam_length + 0.5}" + r""",0);
        
        \end{axis}
    \end{tikzpicture}
    \caption{Shear Force Diagram showing the distribution of shear force along the beam}
    \label{fig:sfd}
\end{figure}

\subsection{SFD Observations}

\begin{itemize}
    \item The shear force is maximum positive at the left support
    \item The shear force decreases linearly under uniformly distributed load
    \item The shear force crosses zero at the midpoint of the beam
    \item The shear force is maximum negative at the right support
    \item The slope of the SFD equals the intensity of the distributed load
\end{itemize}

\newpage
"""
        return sfd_section
    
    def _create_bmd_diagram(self) -> str:
        """
        Create the Bending Moment Diagram using TikZ/pgfplots.
        
        Creates a professional bar chart with colored bars and legend.
        
        Returns:
            String containing LaTeX code for the BMD
        """
        # Prepare coordinates for the bar chart
        coords = ""
        for idx, row in self.data.iterrows():
            x_val = row['x']
            moment = row['Bending Moment']
            coords += f"            ({x_val}, {moment})\n"
        
        bmd_section = r"""
\section{Bending Moment Diagram (BMD)}

The Bending Moment Diagram shows the variation of internal bending moment along 
the length of the beam. Positive (sagging) moments are shown in 
\textcolor{momentpositive}{\textbf{green}}.

\begin{figure}[H]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            width=0.95\textwidth,
            height=8cm,
            xlabel={Position along beam (m)},
            ylabel={Bending Moment (kN$\cdot$m)},
            title={\textbf{Bending Moment Diagram}},
            xmin=-0.5,
            xmax=""" + f"{self.beam_length + 0.5}" + r""",
            ymin=-10,
            ymax=""" + f"{self.data['Bending Moment'].max() + 20}" + r""",
            xtick={""" + ",".join([str(x) for x in self.data['x']]) + r"""},
            grid=both,
            grid style={line width=0.2pt, draw=gray!30},
            major grid style={line width=0.4pt, draw=gray!50},
            axis lines=middle,
            axis line style={->, thick},
            legend style={
                at={(0.98,0.98)},
                anchor=north east,
                draw=black,
                fill=white,
                font=\small
            },
            every axis plot/.append style={thick},
            ybar,
            bar width=8pt,
            enlarge x limits=0.05,
        ]
        
        % Bending Moment (Green)
        \addplot[
            fill=momentpositive,
            draw=momentpositive!80!black,
        ] coordinates {
""" + coords + r"""        };
        \addlegendentry{Bending Moment (Sagging)}
        
        % Zero line
        \draw[black, thick, dashed] (axis cs:-0.5,0) -- (axis cs:""" + f"{self.beam_length + 0.5}" + r""",0);
        
        \end{axis}
    \end{tikzpicture}
    \caption{Bending Moment Diagram showing the distribution of bending moment along the beam}
    \label{fig:bmd}
\end{figure}

\subsection{BMD Observations}

\begin{itemize}
    \item The bending moment is zero at both supports (simply supported conditions)
    \item The bending moment is maximum at the center of the beam (x = """ + f"{self.beam_length/2:.1f}" + r""" m)
    \item Maximum bending moment value: """ + f"{self.data['Bending Moment'].max():.2f}" + r""" kN$\cdot$m
    \item The BMD follows a parabolic curve for uniformly distributed loads
    \item The slope of the BMD at any point equals the shear force at that point
\end{itemize}

\newpage
"""
        return bmd_section
    
    def _create_conclusion(self) -> str:
        """
        Create the conclusion section of the report.
        
        Returns:
            String containing LaTeX code for the conclusion
        """
        max_shear = self.data['Shear force'].abs().max()
        max_moment = self.data['Bending Moment'].max()
        
        conclusion = r"""
% ============================================
% CONCLUSION
% ============================================
\chapter{Conclusion}

\section{Summary of Results}

This structural analysis report has presented a comprehensive analysis of a simply 
supported beam with the following key findings:

\begin{table}[H]
    \centering
    \caption{Summary of Critical Values}
    \vspace{0.5cm}
    \begin{tabular}{|l|c|c|}
        \hline
        \rowcolor{titleblue!20}
        \textbf{Parameter} & \textbf{Value} & \textbf{Location} \\
        \hline
        Maximum Positive Shear & """ + f"{self.data['Shear force'].max():.2f}" + r""" kN & x = 0.0 m \\
        \hline
        Maximum Negative Shear & """ + f"{self.data['Shear force'].min():.2f}" + r""" kN & x = """ + f"{self.beam_length:.1f}" + r""" m \\
        \hline
        Maximum Bending Moment & """ + f"{max_moment:.2f}" + r""" kN$\cdot$m & x = """ + f"{self.beam_length/2:.1f}" + r""" m \\
        \hline
    \end{tabular}
\end{table}

\section{Design Recommendations}

Based on the analysis results, the following recommendations are made for the 
design of this simply supported beam:

\begin{enumerate}
    \item \textbf{Shear Reinforcement:} Provide adequate shear reinforcement near 
          the supports where shear forces are maximum.
    
    \item \textbf{Flexural Reinforcement:} Provide maximum flexural reinforcement 
          at the midspan where the bending moment is maximum.
    
    \item \textbf{Deflection Check:} Verify that the beam deflection under service 
          loads is within acceptable limits.
    
    \item \textbf{Support Design:} Design the supports to safely transfer the 
          reaction forces to the foundation.
\end{enumerate}

\section{Report Generation}

This report was automatically generated using:
\begin{itemize}
    \item Python for data processing and LaTeX generation
    \item TikZ/PGFPlots for vector graphics diagrams
    \item \LaTeX{} for professional document formatting
\end{itemize}

\end{document}
"""
        return conclusion
    
    def generate_report(self) -> str:
        """
        Generate the complete LaTeX document and compile to PDF.
        
        This method orchestrates the entire report generation process:
        1. Loads data from Excel
        2. Generates all LaTeX sections
        3. Writes the .tex file
        4. Compiles to PDF using pdflatex
        
        Returns:
            Path to the generated PDF file
        """
        print("=" * 60)
        print("BEAM ANALYSIS REPORT GENERATOR")
        print("=" * 60)
        
        # Step 1: Load the data
        self.load_data()
        
        # Step 2: Generate LaTeX content
        print("[INFO] Generating LaTeX document...")
        
        latex_content = ""
        latex_content += self._create_preamble()
        latex_content += self._create_title_page()
        latex_content += self._create_toc()
        latex_content += self._create_introduction()
        latex_content += self._create_data_table()
        latex_content += self._create_sfd_diagram()
        latex_content += self._create_bmd_diagram()
        latex_content += self._create_conclusion()
        
        # Step 3: Write the .tex file
        tex_path = os.path.join(os.path.dirname(self.excel_path), f"{self.output_name}.tex")
        
        print(f"[INFO] Writing LaTeX file: {tex_path}")
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Step 4: Compile to PDF
        print("[INFO] Compiling LaTeX to PDF...")
        output_dir = os.path.dirname(self.excel_path)
        
        # Run pdflatex twice for TOC and references
        for run in range(2):
            print(f"[INFO] pdflatex run {run + 1}/2...")
            result = os.system(
                f'cd /d "{output_dir}" && pdflatex -interaction=nonstopmode "{self.output_name}.tex"'
            )
            if result != 0:
                print(f"[WARNING] pdflatex returned non-zero exit code: {result}")
        
        pdf_path = os.path.join(output_dir, f"{self.output_name}.pdf")
        
        if os.path.exists(pdf_path):
            print("=" * 60)
            print(f"[SUCCESS] PDF generated: {pdf_path}")
            print("=" * 60)
        else:
            print("[ERROR] PDF generation failed. Check the .tex file for errors.")
        
        # Clean up auxiliary files
        self._cleanup_aux_files(output_dir)
        
        return pdf_path
    
    def _cleanup_aux_files(self, output_dir: str) -> None:
        """
        Clean up auxiliary files generated by LaTeX compilation.
        
        Args:
            output_dir: Directory containing the auxiliary files
        """
        aux_extensions = ['.aux', '.log', '.out', '.toc']
        
        for ext in aux_extensions:
            aux_file = os.path.join(output_dir, f"{self.output_name}{ext}")
            if os.path.exists(aux_file):
                try:
                    os.remove(aux_file)
                    print(f"[INFO] Cleaned up: {aux_file}")
                except Exception as e:
                    print(f"[WARNING] Could not remove {aux_file}: {e}")


def main():
    """
    Main entry point for the Beam Analysis Report Generator.
    """
    # Define file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    excel_path = os.path.join(script_dir, "Force Table.xlsx")
    beam_image_path = os.path.join(script_dir, "simply_supported_beam.png")
    output_name = "Beam_Analysis_Report"
    
    # Verify input files exist
    if not os.path.exists(excel_path):
        print(f"[ERROR] Excel file not found: {excel_path}")
        return
    
    if not os.path.exists(beam_image_path):
        print(f"[ERROR] Beam image not found: {beam_image_path}")
        return
    
    # Create and run the report generator
    generator = BeamReportGenerator(
        excel_path=excel_path,
        beam_image_path=beam_image_path,
        output_name=output_name
    )
    
    pdf_path = generator.generate_report()
    
    print("\n[INFO] Report generation complete!")
    print(f"[INFO] Output file: {pdf_path}")


if __name__ == "__main__":
    main()
