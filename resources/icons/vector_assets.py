from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QCursor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import QWidget


def create_course_pixmap(art_key: str, width: int, height: int, radius: int = 14) -> QPixmap:
    """Desenha miniaturas vetoriais nítidas para cada curso (fallback para imagens do Storage)."""
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    clip = QPainterPath()
    clip.addRoundedRect(QRectF(0, 0, width, height), radius, radius)
    painter.setClipPath(clip)

    if art_key == "ai":
        grad = QLinearGradient(0, 0, width, height)
        grad.setColorAt(0.0, QColor("#041024"))
        grad.setColorAt(1.0, QColor("#0B2A4A"))
        painter.fillRect(0, 0, width, height, grad)

        painter.setPen(QPen(QColor("#0EA5E9"), 1.6))
        cx, cy = width / 2, height / 2
        lines = [
            ((width * 0.06, height * 0.22), (width * 0.28, height * 0.22), (width * 0.34, height * 0.34)),
            ((width * 0.08, height * 0.78), (width * 0.30, height * 0.78), (width * 0.36, height * 0.65)),
            ((width * 0.94, height * 0.26), (width * 0.72, height * 0.26), (width * 0.66, height * 0.38)),
            ((width * 0.92, height * 0.76), (width * 0.70, height * 0.76), (width * 0.64, height * 0.64)),
        ]
        for p1, p2, p3 in lines:
            painter.drawLine(QPointF(*p1), QPointF(*p2))
            painter.drawLine(QPointF(*p2), QPointF(*p3))
            painter.setBrush(QColor("#38BDF8"))
            painter.drawEllipse(QPointF(*p1), 3.5, 3.5)
            painter.setBrush(Qt.NoBrush)

        chip_size = min(width, height) * 0.50
        chip_rect = QRectF(cx - chip_size / 2, cy - chip_size / 2, chip_size, chip_size)
        painter.setBrush(QColor("#0C2D57"))
        painter.setPen(QPen(QColor("#38BDF8"), 2.2))
        painter.drawRoundedRect(chip_rect, 10, 10)

        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Arial", max(16, int(chip_size * 0.42)), QFont.Bold))
        painter.drawText(chip_rect, Qt.AlignCenter, "AI")

    elif art_key == "db":
        painter.fillRect(0, 0, width, height, QColor("#FFFFFF"))
        cx, cy = width / 2, height * 0.62
        rx, ry = width * 0.22, height * 0.085
        painter.setPen(Qt.NoPen)
        blocks = [
            (cx - rx * 0.55, height * 0.14, 11, "#1D4ED8"),
            (cx + rx * 0.05, height * 0.18, 12, "#0284C7"),
            (cx + rx * 0.60, height * 0.14, 10, "#1E3A8A"),
            (cx - rx * 0.15, height * 0.28, 9, "#38BDF8"),
        ]
        for bx, by, sz, color in blocks:
            painter.setBrush(QColor(color))
            painter.drawRoundedRect(QRectF(bx, by, sz, sz), 2, 2)

        layers = [
            (cy + ry * 2.2, "#172554"),
            (cy + ry * 0.7, "#1E40AF"),
            (cy - ry * 0.8, "#1D4ED8"),
        ]
        for ly, col in layers:
            painter.setBrush(QColor(col))
            painter.drawRoundedRect(QRectF(cx - rx, ly - ry, rx * 2, ry * 2.1), 8, 8)
            painter.setBrush(QColor("#0284C7"))
            painter.drawEllipse(QPointF(cx, ly - ry), rx, ry * 0.7)

    elif art_key == "python":
        painter.fillRect(0, 0, width, height, QColor("#FFFFFF"))
        cx, cy = width / 2, height / 2
        s = min(width, height) * 0.26

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#3776AB"))
        painter.drawRoundedRect(QRectF(cx - s * 0.95, cy - s * 1.25, s * 1.55, s * 1.15), 14, 14)
        painter.drawRoundedRect(QRectF(cx - s * 1.35, cy - s * 0.45, s * 1.15, s * 0.95), 12, 12)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(QPointF(cx - s * 0.45, cy - s * 0.90), 4.0, 4.0)

        painter.setBrush(QColor("#FFD43B"))
        painter.drawRoundedRect(QRectF(cx - s * 0.60, cy + s * 0.10, s * 1.55, s * 1.15), 14, 14)
        painter.drawRoundedRect(QRectF(cx + s * 0.20, cy - s * 0.50, s * 1.15, s * 0.95), 12, 12)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(QPointF(cx + s * 0.45, cy + s * 0.90), 4.0, 4.0)

    else:
        grad = QLinearGradient(0, 0, width, height)
        grad.setColorAt(0.0, QColor("#3B2F2F"))
        grad.setColorAt(1.0, QColor("#7C5A43"))
        painter.fillRect(0, 0, width, height, grad)

        cx, cy = width / 2, height / 2
        r = min(width, height) * 0.30
        painter.setPen(QPen(QColor("#93C5FD"), 1.6, Qt.DashLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), r, r)

        painter.setPen(Qt.NoPen)
        offsets = [
            (0, -r), (r * 0.86, -r * 0.5), (r * 0.86, r * 0.5),
            (0, r), (-r * 0.86, r * 0.5), (-r * 0.86, -r * 0.5),
        ]
        for i, (dx, dy) in enumerate(offsets):
            painter.setBrush(QColor("#38BDF8" if i % 2 == 0 else "#60A5FA"))
            painter.drawEllipse(QPointF(cx + dx, cy + dy), 7, 7)

        center_box = QRectF(cx - 22, cy - 17, 44, 34)
        painter.setBrush(QColor("#0F172A"))
        painter.setPen(QPen(QColor("#BAE6FD"), 1.5))
        painter.drawRoundedRect(center_box, 8, 8)
        painter.setPen(QColor("#E0F2FE"))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(center_box, Qt.AlignCenter, "☁")

    painter.end()
    return pixmap


class TechLogoIcon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(46, 38)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        blue = QColor("#6155F5")

        p.setPen(QPen(blue, 2.4))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(4, 3, 38, 23), 3, 3)

        p.setPen(Qt.NoPen)
        p.setBrush(blue)
        base = QPainterPath()
        base.moveTo(18, 26)
        base.lineTo(28, 26)
        base.lineTo(31, 34)
        base.lineTo(15, 34)
        base.closeSubpath()
        p.drawPath(base)

        cap = QPainterPath()
        cap.moveTo(23, 7)
        cap.lineTo(34, 12)
        cap.lineTo(23, 17)
        cap.lineTo(12, 12)
        cap.closeSubpath()
        p.drawPath(cap)

        p.setPen(QPen(blue, 2.0))
        p.drawArc(QRectF(17, 13, 12, 8), 180 * 16, 180 * 16)
        p.end()


class AvatarWidget(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        self.clicked.emit()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#09090B"))
        p.drawEllipse(QRectF(1, 1, 36, 36))

        p.setBrush(QColor("#FFFFFF"))
        p.drawEllipse(QPointF(19, 13), 5.2, 5.2)
        p.drawPie(QRectF(9, 20, 20, 18), 0, 180 * 16)

        p.setBrush(QColor("#B80D57"))
        p.setPen(QPen(QColor("#FFFFFF"), 2.0))
        p.drawEllipse(QPointF(33, 33), 5.0, 5.0)
        p.end()


class RadioIndicator(QWidget):
    def __init__(self, selected: bool = False, parent=None):
        super().__init__(parent)
        self._selected = selected
        self.setFixedSize(22, 22)

    def set_selected(self, value: bool):
        self._selected = value
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        border_color = QColor("#B80D57") if self._selected else QColor("#CBD5E1")
        p.setPen(QPen(border_color, 2.0))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(QRectF(2, 2, 18, 18))

        if self._selected:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor("#B80D57"))
            p.drawEllipse(QPointF(11, 11), 5.2, 5.2)
        p.end()


class CheckmarkBadge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(88, 88)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#F9EDF2"))
        p.drawEllipse(QRectF(2, 2, 84, 84))

        p.setBrush(QColor("#B80D57"))
        p.drawEllipse(QRectF(17, 17, 54, 54))

        pen = QPen(QColor("#FFFFFF"), 3.6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        p.setPen(pen)
        p.drawLine(QPointF(33, 45), QPointF(41, 53))
        p.drawLine(QPointF(41, 53), QPointF(56, 36))
        p.end()