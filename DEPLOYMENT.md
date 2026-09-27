# Vaa reviewer deployment (Railway)

This setup is for a small demo using the existing FastAPI API, SQLite schema,
and seed fixture. It does not copy the local `child_development.db` to the
cloud, and it does not seed automatically on each deploy.

## One-time service setup

1. Create a Railway project and deploy this repository from its root. The
   `Dockerfile` installs the pinned Python requirements and includes the
   existing assessment document and therapist video.
2. Attach one persistent volume to the service at `/data`. Keep the service at
   one replica and one Uvicorn worker. Start with a 2 GB volume; increase it if
   voice recordings accumulate. For CPU Whisper transcription, allocate about
   2 GB of service memory if available; transcription may be slow on CPU.
3. Configure these service variables in Railway. Do not put secrets in this
   file or in Flutter:

   | Variable | Value |
   | --- | --- |
   | `APP_ENV` | `production` |
   | `JWT_SECRET_KEY` | A new, unique random value of at least 32 characters |
   | `DATABASE_URL` | `sqlite:////data/child_development.db` |
   | `VOICE_STORAGE_DIR` | `/data/audio` |
   | `HF_HOME` | `/data/huggingface` |
   | `WHISPER_MODEL` | `base` |
   | `WHISPER_DEVICE` | `cpu` |
   | `WHISPER_COMPUTE_TYPE` | `int8` |
   | `CORS_ORIGINS` | Leave empty for the native Android APK; otherwise enter exact trusted web origins, comma-separated |
   | `DEMO_ADMIN_PASSWORD` | A unique random demo password, at least 16 characters |
   | `DEMO_PARENT_PASSWORD` | A different unique random demo password, at least 16 characters |
   | `DEMO_THERAPIST_PASSWORD` | A third unique random demo password, at least 16 characters |

   Railway supplies `PORT`. Do not set it to a fixed value.
4. Set the service health check path to `/health`; `railway.toml` contains the
   same setting. Generate a Railway public domain. Railway provisions HTTPS
   for that domain.
5. After the `/data` volume is attached and the service starts, run this once
   in the Railway service shell:

   ```sh
   python -m app.database.seed_demo
   ```

   It refuses to run if any application table already contains data. It
   initializes the existing fixture and imports the existing LDST assessment
   document. Seed scripts never print passwords. The
   three `DEMO_*_PASSWORD` variables must be set for this one-time command.
   After successful seeding, those three variables may be removed; the
   passwords are already hashed in the user records.

Do not configure `seed.py` as a startup, build, or pre-deploy command. It drops
and recreates every table. The cloud database is a fresh demo database; the
existing local SQLite database is not uploaded.

## Seeded reviewer accounts

The fixture creates:

- Admin: `admin@test.com`
- Parents: `parent1@test.com`, `parent2@test.com`, `parent3@test.com`
- Therapists: `therapist1@test.com`, `therapist2@test.com`,
  `therapist3@test.com`

All parent and therapist accounts of the same role use that role's configured
demo password. The fixture includes seven children, assignments, assessment
sessions/results, development profiles, recommendations, goals, milestones,
and progress. It does not create fabricated voice recordings; test voice by
uploading a recording after deployment. Do not load real child or clinical
records into this reviewer demo.

## Flutter commands

Local development can continue using the local API, for example:

```sh
flutter run --dart-define=API_BASE_URL=http://192.168.1.x:8000
```

After the Railway service is healthy, replace the example URL with its actual
HTTPS domain and build the reviewer APK:

```sh
flutter build apk --release --dart-define=API_BASE_URL=https://<railway-domain>
```

The APK embeds the API URL at build time. A placeholder or local IP must not be
used for the reviewer build. Android cleartext HTTP is enabled only for debug
builds; release builds require HTTPS.

## Storage, database, and voice notes

SQLite remains in use. For this small demo, keep it on the persistent `/data`
volume, with one service instance and one worker; do not horizontally scale this
SQLite deployment. `Base.metadata.create_all()` creates missing tables at
startup, but it does not migrate existing schema changes. Take a volume backup
before replacing or changing the demo database.

Voice recordings use `/data/audio` and the Whisper model cache uses
`/data/huggingface`, so both survive container replacement. The therapist video
is copied into the image. `faster-whisper` uses PyAV for audio decoding, so a
system FFmpeg executable is not required for basic transcription. The model is
downloaded the first time it is needed; allow outbound network access and
enough volume space. CPU inference can be slow, and a 0.5 GB service may run out
of memory once the model loads. If transcription fails, the existing API keeps
the original audio and returns it for authorized playback.

## Authorization and CORS

JWT and role checks remain enabled. Production startup fails if
`APP_ENV=production` is set without a unique `JWT_SECRET_KEY` of at least 32
characters. The API accepts only exact `CORS_ORIGINS` entries and rejects `*`.
The native APK does not use browser CORS; leave the variable empty unless a web
client needs access.

## Manual steps still required

- Create the Railway account/project, connect or upload the repository, attach
  the `/data` volume, and enter the variables above.
- Choose a service memory size that can run CPU Whisper. Railway's free-tier
  limit is too small to rely on for Whisper; a paid plan may cost more than its
  monthly minimum based on actual CPU/RAM usage.
- Run the one-time seed command and check `/health` and the generated HTTPS
  domain.
- Build the release APK after the real domain is known, then distribute the
  APK and demo credentials privately.
