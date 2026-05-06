from dotenv import load_dotenv
from functions import Assistant
from livekit import agents, rtc
from livekit.agents import (
    AgentServer,
    AgentSession,
    inference,
    room_io,
)
from livekit.plugins import (
    google,
    noise_cancellation,
)
from prompts import greetingInstructions

load_dotenv()

server = AgentServer()


@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            voice="Aoede",
            temperature=0.8,
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
            # video_input=True,
        ),
    )

    await session.generate_reply(instructions=greetingInstructions)


if __name__ == "__main__":
    agents.cli.run_app(server)
