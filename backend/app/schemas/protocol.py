# -*- coding: utf-8 -*-
from typing import Literal, Optional
from uuid import UUID, uuid4

import pydantic
from pydantic import BaseModel


class TaskRequest(BaseModel):
    """The frontend asks the backend for a task."""

    type: str
    user_id: Optional[str] = None


class GenericTaskRequest(TaskRequest):
    type: Literal["generic"] = "generic"


class Task(BaseModel):
    """A task is a unit of work that the backend gives to the frontend."""

    id: UUID = pydantic.Field(default_factory=uuid4)
    type: str
    addressed_users: Optional[list[str]] = None


class TaskResponse(BaseModel):
    """A task response is a message from the frontend to acknowledge the given task."""

    type: str
    status: Literal["success", "failure"]


class PostCreatedTaskResponse(TaskResponse):
    type: Literal["post_created"] = "post_created"
    post_id: str


class SummarizeStoryTask(Task):
    type: Literal["summarize_story"] = "summarize_story"
    story: str


class TaskDone(Task):
    type: Literal["task_done"] = "task_done"
    reply_to_post_id: str


class Interaction(BaseModel):
    """An interaction is a message from the frontend to the backend."""

    type: str
    user_id: str


class TextReplyToPost(Interaction):
    """A user has replied to a post with text."""

    type: Literal["text_reply_to_post"] = "text_reply_to_post"
    post_id: str
    user_post_id: str
    text: str
