try:
    from portia.builder.plan_builder_v2 import PlanBuilderV2
    from pydantic import BaseModel
except Exception:
    PlanBuilderV2 = None

if PlanBuilderV2:
    class Result(BaseModel):
        shortlisted: int
    builder = PlanBuilderV2(label="JobMatch - Portia plan")
    # builder.input(...), add llm_step, tool invocations, clarifications...
    plan = builder.build()
else:
    plan = None
