import os
import html

class BaseWidget:
    def is_applicable(self, raw_query, results):
        raise NotImplementedError()

    def render_html(self, raw_query, results):
        raise NotImplementedError()


class ImageGalleryWidget(BaseWidget):
    def is_applicable(self, raw_query, results):
        return any(self._is_image(r["file_path"]) for r in results)

    def render_html(self, raw_query, results):
        image_paths = [
            r["file_path"] for r in results
            if self._is_image(r["file_path"])
        ]
        items = []
        for path in image_paths:
            escaped_path = html.escape(path)
            filename = os.path.basename(path)
            items.append(
                f'<div class="widget-image-item">'
                f'  <img src="file:///{escaped_path}" '
                f'       alt="{html.escape(filename)}" />'
                f'</div>'
            )

        return (
            '<div class="widget widget-image-gallery">\n'
            '  <h3>Image Gallery</h3>\n'
            '  <div class="gallery-container">\n'
            f'    {"".join(items)}\n'
            '  </div>\n'
            '</div>\n'
        )

    def _is_image(self, path):
        ext = os.path.splitext(path.lower())[1]
        return ext in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"}


class LogViewerWidget(BaseWidget):
    def is_applicable(self, raw_query, results):
        return any(r["file_path"].lower().endswith(".log") for r in results)

    def render_html(self, raw_query, results):
        log_files = [
            r["file_path"] for r in results
            if r["file_path"].lower().endswith(".log")
        ]
        items = []
        for path in log_files:
            try:
                preview_lines = []
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f):
                        if i >= 50:
                            break
                        preview_lines.append(html.escape(line.rstrip("\n")))
                snippet = "<br/>".join(preview_lines)
            except Exception:
                snippet = "<i>Could not read file.</i>"

            filename = os.path.basename(path)
            items.append(
                '<div class="log-file-block">\n'
                f'  <h4>{html.escape(filename)}</h4>\n'
                f'  <div class="log-snippet">{snippet}</div>\n'
                '</div>\n'
            )

        return (
            '<div class="widget widget-log-viewer">\n'
            '  <h3>Log Viewer</h3>\n'
            f'  {"".join(items)}\n'
            '</div>\n'
        )


class WordCountWidget(BaseWidget):
    def is_applicable(self, raw_query, results):
        text_exts = {".txt", ".md", ".log", ".csv", ".py", ".java", ".html", ".css", ".js"}
        return any(
            os.path.splitext(r["file_path"].lower())[1] in text_exts
            for r in results
        )

    def render_html(self, raw_query, results):
        total_words = 0
        for r in results:
            ext = os.path.splitext(r["file_path"].lower())[1]
            if ext in {".txt", ".md", ".log", ".csv", ".py", ".java", ".html", ".css", ".js"}:
                content = r.get("file_content") or ""
                total_words += len(content.split())

        return (
            '<div class="widget widget-word-count">\n'
            '  <h3>Word Count</h3>\n'
            f'  <p>Total words across text files: <strong>{total_words}</strong></p>\n'
            '</div>\n'
        )


class DirectoryStatsWidget(BaseWidget):
    def is_applicable(self, raw_query, results):
        return len(results) > 0

    def render_html(self, raw_query, results):
        dirs = set(os.path.dirname(r["file_path"]) for r in results)
        distinct_dirs = len(dirs)
        return (
            '<div class="widget widget-dir-stats">\n'
            '  <h3>Directory Statistics</h3>\n'
            f'  <p>Distinct directories in results: <strong>{distinct_dirs}</strong></p>\n'
            '</div>\n'
        )


class CalculatorWidget(BaseWidget):
    def is_applicable(self, raw_query, results):
        return "calculator" in raw_query.lower()

    def render_html(self, raw_query, results):
        return (
            '<div class="widget widget-calculator">\n'
            '  <h3>Calculator</h3>\n'
            '  <input type="text" id="calc-input" placeholder="Enter expression" />\n'
            '  <button onclick="evalCalc()">=</button>\n'
            '  <div id="calc-output"></div>\n'
            '  <script>\n'
            '    function evalCalc() {\n'
            '      try {\n'
            '        var exp = document.getElementById("calc-input").value;\n'
            '        var res = eval(exp);\n'
            '        document.getElementById("calc-output").textContent = res;\n'
            '      } catch(e) {\n'
            '        document.getElementById("calc-output").textContent = "Error";\n'
            '      }\n'
            '    }\n'
            '  </script>\n'
            '</div>\n'
        )


class WidgetFactory:
    def __init__(self):
        self._all_widgets = [
            ImageGalleryWidget(),
            LogViewerWidget(),
            WordCountWidget(),
            DirectoryStatsWidget(),
            CalculatorWidget()
        ]

    def get_widgets(self, raw_query, results):
        html_fragments = []
        for w in self._all_widgets:
            if w.is_applicable(raw_query, results):
                html_fragments.append(w.render_html(raw_query, results))
        return html_fragments
