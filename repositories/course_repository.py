from typing import Dict, List, Optional, Set

from config.database import get_supabase_client
from models.class_model import CourseClass, Lesson
from models.course import Course


class CourseRepository:
    def __init__(self) -> None:
        self._client = get_supabase_client()
        self._local_courses: List[Course] = self._build_seed_courses()
        self._local_lessons: Dict[int, List[Lesson]] = self._build_seed_lessons()
        self._course_classes: List[CourseClass] = [
            CourseClass(
                code="A",
                title="Turma A — 25/11",
                short_schedule="Ter e Qui • 19h às 21h",
                start_date="25 de novembro de 2026",
                full_schedule="Ter e Qui - 19h às 21h",
            ),
            CourseClass(
                code="B",
                title="Turma B — 02/12",
                short_schedule="Sábados • 08h às 12h",
                start_date="02 de dezembro de 2026",
                full_schedule="Sábados - 08h às 12h",
            ),
        ]

    def list_active_courses(self) -> List[Course]:
        if self._client:
            try:
                resp = (
                    self._client.table("curso")
                    .select("*")
                    .eq("ativo", True)
                    .order("id_curso")
                    .execute()
                )
                if resp.data:
                    courses = [Course.from_dict(row) for row in resp.data]
                    self._enrich_visual_defaults(courses)
                    return courses
            except Exception as exc:
                print(f"[CourseRepository] Erro Supabase em list_active_courses: {exc}")

        return [c for c in self._local_courses if c.active]

    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        for course in self.list_active_courses():
            if course.course_id == course_id:
                return course
        return None

    def list_lessons_by_course(self, course_id: int) -> List[Lesson]:
        if self._client:
            try:
                resp = (
                    self._client.table("aula")
                    .select("*")
                    .eq("id_curso", course_id)
                    .order("ordem")
                    .execute()
                )
                if resp.data:
                    return [Lesson.from_dict(row) for row in resp.data]
            except Exception as exc:
                print(f"[CourseRepository] Erro Supabase em list_lessons_by_course: {exc}")

        return list(self._local_lessons.get(course_id, []))

    def list_course_classes(self) -> List[CourseClass]:
        return list(self._course_classes)

    def list_favorite_course_ids(self, user_id: str) -> Set[int]:
        if self._client:
            try:
                resp = (
                    self._client.table("favorito")
                    .select("id_curso")
                    .eq("id_usuario", user_id)
                    .execute()
                )
                if resp.data is not None:
                    return {int(row["id_curso"]) for row in resp.data}
            except Exception as exc:
                print(f"[CourseRepository] Erro Supabase em list_favorite_course_ids: {exc}")
        return set()

    def add_favorite(self, user_id: str, course_id: int) -> None:
        if self._client:
            try:
                payload = {"id_usuario": user_id, "id_curso": course_id}
                (
                    self._client.table("favorito")
                    .upsert(payload, on_conflict="id_usuario,id_curso")
                    .execute()
                )
            except Exception as exc:
                print(f"[CourseRepository] Erro Supabase em add_favorite: {exc}")

    def remove_favorite(self, user_id: str, course_id: int) -> None:
        if self._client:
            try:
                (
                    self._client.table("favorito")
                    .delete()
                    .eq("id_usuario", user_id)
                    .eq("id_curso", course_id)
                    .execute()
                )
            except Exception as exc:
                print(f"[CourseRepository] Erro Supabase em remove_favorite: {exc}")

    def _enrich_visual_defaults(self, courses: List[Course]) -> None:
        art_cycle = ["ai", "db", "python", "office"]
        for idx, course in enumerate(courses):
            if not course.art_key:
                course.art_key = art_cycle[idx % len(art_cycle)]
            if not course.learnings:
                course.learnings = [
                    "Aplicar os conceitos do curso em projetos práticos.",
                    "Acompanhar aulas gravadas no YouTube e materiais complementares.",
                    "Consolidar os conhecimentos com exercícios guiados.",
                ]

    @staticmethod
    def _build_seed_courses() -> List[Course]:
        return [
            Course(
                course_id=1,
                category_id=1,
                name="Dominando o Uso de IA",
                summary="Do básico ao avançado em Inteligência Artificial.",
                description="Aprenda a utilizar Inteligência Artificial de forma prática para estudos, trabalho e produtividade.",
                workload_hours=20,
                level="Iniciante/Intermediário",
                price=199.00,
                active=True,
                art_key="ai",
                learnings=[
                    "Criar comandos claros e estruturados para obter respostas precisas.",
                    "Acelerar pesquisas, resumos, revisão de textos e organização diária.",
                    "Integrar ferramentas de IA no dia a dia profissional com segurança.",
                ],
            ),
            Course(
                course_id=2,
                category_id=2,
                name="Desmitificando Estrutura de Dados",
                summary="Aprendizagem completa: teoria e prática.",
                description="Domine listas, pilhas, filas, árvores, grafos e análise de complexidade com exemplos práticos.",
                workload_hours=24,
                level="Intermediário",
                price=160.00,
                active=True,
                art_key="db",
                learnings=[
                    "Escolher a estrutura ideal para cada tipo de problema.",
                    "Melhorar o desempenho e o uso de memória das suas aplicações.",
                    "Resolver desafios técnicos e entrevistas de programação.",
                ],
            ),
            Course(
                course_id=3,
                category_id=2,
                name="Programação com Python",
                summary="Introdução à lógica e ao desenvolvimento de projetos.",
                description="Comece do zero em Python, aprenda lógica de programação e construa projetos reais passo a passo.",
                workload_hours=18,
                level="Básico",
                price=85.00,
                active=True,
                art_key="python",
                learnings=[
                    "Escrever código Python limpo e organizado desde o início.",
                    "Automatizar tarefas repetitivas com scripts simples.",
                    "Estruturar pequenos aplicativos desktop e scripts práticos.",
                ],
            ),
            Course(
                course_id=4,
                category_id=3,
                name="Produtividade digital",
                summary="Office, nuvem, ferramentas de colaboração",
                description="Domine ferramentas de escritório, armazenamento em nuvem e colaboração em equipe para render mais.",
                workload_hours=12,
                level="Básico",
                price=65.00,
                active=True,
                art_key="office",
                learnings=[
                    "Trabalhar de forma colaborativa na nuvem sem perder versões.",
                    "Criar planilhas e documentos claros em menos tempo.",
                    "Manter e-mails, tarefas e calendários organizados.",
                ],
            ),
        ]

    @staticmethod
    def _build_seed_lessons() -> Dict[int, List[Lesson]]:
        return {
            1: [
                Lesson(101, 1, "Aula 01 — Introdução à IA Generativa", "Conceitos fundamentais de LLMs.", 1, 25, "https://www.youtube.com/"),
                Lesson(102, 1, "Aula 02 — Estrutura de prompts eficazes", "Engenharia de prompts na prática.", 2, 30, "https://www.youtube.com/"),
                Lesson(103, 1, "Aula 03 — IA aplicada a documentos e planilhas", "Fluxos de produtividade.", 3, 35, "https://www.youtube.com/"),
                Lesson(104, 1, "Aula 04 — Automação de fluxos de trabalho", "Integrações no dia a dia.", 4, 40, "https://www.youtube.com/"),
                Lesson(105, 1, "Aula 05 — Boas práticas e uso ético", "Privacidade e verificação.", 5, 25, "https://www.youtube.com/"),
                Lesson(106, 1, "Aula 06 — Projeto prático final", "Entrega e revisão.", 6, 45, "https://www.youtube.com/"),
            ],
            2: [
                Lesson(201, 2, "Aula 01 — Memória, arrays e complexidade", "Análise Big-O.", 1, 35, "https://www.youtube.com/"),
                Lesson(202, 2, "Aula 02 — Listas encadeadas na prática", "Ponteiros e nós.", 2, 40, "https://www.youtube.com/"),
                Lesson(203, 2, "Aula 03 — Pilhas e filas em aplicações reais", "LIFO e FIFO.", 3, 35, "https://www.youtube.com/"),
                Lesson(204, 2, "Aula 04 — Tabelas Hash e Árvores Binárias", "Buscas eficientes.", 4, 45, "https://www.youtube.com/"),
                Lesson(205, 2, "Aula 05 — Introdução a grafos", "BFS e DFS.", 5, 45, "https://www.youtube.com/"),
                Lesson(206, 2, "Aula 06 — Exercícios integradores", "Resolução comentada.", 6, 40, "https://www.youtube.com/"),
            ],
            3: [
                Lesson(301, 3, "Aula 01 — Configurando o ambiente Python", "Instalação e venv.", 1, 20, "https://www.youtube.com/"),
                Lesson(302, 3, "Aula 02 — Lógica, variáveis e operadores", "Tipos básicos.", 2, 30, "https://www.youtube.com/"),
                Lesson(303, 3, "Aula 03 — Estruturas de decisão e repetição", "if, for e while.", 3, 35, "https://www.youtube.com/"),
                Lesson(304, 3, "Aula 04 — Funções e módulos", "Organização de código.", 4, 30, "https://www.youtube.com/"),
                Lesson(305, 3, "Aula 05 — Manipulação de arquivos", "Leitura e escrita.", 5, 30, "https://www.youtube.com/"),
                Lesson(306, 3, "Aula 06 — Mini-projeto guiado", "Aplicação completa.", 6, 45, "https://www.youtube.com/"),
            ],
            4: [
                Lesson(401, 4, "Aula 01 — Fundamentos da nuvem", "Sincronização e pastas.", 1, 20, "https://www.youtube.com/"),
                Lesson(402, 4, "Aula 02 — Documentos colaborativos", "Edição em equipe.", 2, 25, "https://www.youtube.com/"),
                Lesson(403, 4, "Aula 03 — Planilhas para controle diário", "Fórmulas essenciais.", 3, 30, "https://www.youtube.com/"),
                Lesson(404, 4, "Aula 04 — Gestão de agenda e reuniões", "Calendários compartilhados.", 4, 20, "https://www.youtube.com/"),
                Lesson(405, 4, "Aula 05 — Fluxo semanal de produtividade", "Atalhos e rotinas.", 5, 25, "https://www.youtube.com/"),
                Lesson(406, 4, "Aula 06 — Checklist final", "Revisão prática.", 6, 20, "https://www.youtube.com/"),
            ],
        }