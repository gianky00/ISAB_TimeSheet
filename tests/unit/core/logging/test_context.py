import threading

from src.application.services.logging.context import (
    generate_span_id,
    generate_trace_id,
    get_context,
    get_current_audit_id,
    get_current_span_id,
    get_current_trace_id,
    set_audit_id,
    with_context,
)


class TestLoggingContext:
    def test_set_get_has_clear(self):
        ctx = get_context()
        ctx.clear()

        ctx.set("key1", "val1")
        assert ctx.get("key1") == "val1"
        assert ctx.has("key1") is True

        ctx.clear()
        assert ctx.get("key1") is None
        assert ctx.has("key1") is False

    def test_thread_isolation(self):
        ctx = get_context()
        ctx.clear()
        ctx.set("main", "true")

        results = {}

        def thread_func():
            t_ctx = get_context()
            t_ctx.set("thread", "true")
            results["thread_val"] = t_ctx.get("thread")
            results["main_val"] = t_ctx.get("main")

        t = threading.Thread(target=thread_func)
        t.start()
        t.join()

        assert results["thread_val"] == "true"
        assert results["main_val"] is None  # Isolamento thread
        assert ctx.get("main") == "true"
        assert ctx.get("thread") is None

    def test_with_context_nesting(self):
        ctx = get_context()
        ctx.clear()

        with with_context(user="mario", trace_id="T1"):
            assert ctx.get("user") == "mario"
            assert get_current_trace_id() == "T1"

            with with_context(user="luigi"):
                assert ctx.get("user") == "luigi"
                assert get_current_trace_id() == "T1"  # Ereditato

            assert ctx.get("user") == "mario"  # Ripristinato

        assert ctx.get("user") is None

    def test_generate_ids(self):
        tid = generate_trace_id()
        assert tid.startswith("trace_")
        assert len(tid) > 10

        sid = generate_span_id()
        assert sid.startswith("span_")

    def test_audit_id_helpers(self):
        get_context().clear()
        set_audit_id(123)
        assert get_current_audit_id() == 123
        assert get_context().get("audit_id") == 123

    def test_current_span_id(self):
        get_context().clear()
        assert get_current_span_id() is None

        with with_context(span_id="S1"):
            assert get_current_span_id() == "S1"
