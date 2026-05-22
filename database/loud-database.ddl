CREATE SCHEMA IF NOT EXISTS content;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS content.venue (
    id          UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    city        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.event (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    venue_id        UUID        NOT NULL,
    title           VARCHAR(80) NOT NULL,
    starts_at       TIMESTAMP WITH TIME ZONE,
    description     VARCHAR(500),
    min_price       DECIMAL(10, 2),
    total_capacity  INTEGER     NOT NULL DEFAULT 0,
    available       INTEGER     NOT NULL DEFAULT 0,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified_at     TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_event_venue
        FOREIGN KEY (venue_id) REFERENCES content.venue(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS content.ticket_type (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id        UUID        NOT NULL,
    name            VARCHAR(50) NOT NULL,
    price           DECIMAL(10, 2) NOT NULL,
    total_capacity  INTEGER     NOT NULL DEFAULT 0,
    available       INTEGER     NOT NULL DEFAULT 0,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified_at     TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_ticket_type_event
        FOREIGN KEY (event_id) REFERENCES content.event(id) ON DELETE CASCADE,

    CONSTRAINT chk_ticket_type_available
        CHECK (available >= 0 AND available <= total_capacity)
);

CREATE TABLE IF NOT EXISTS content.order (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_name   VARCHAR(255) NOT NULL,
    customer_email  VARCHAR(255) NOT NULL,
    total           DECIMAL(10, 2) NOT NULL DEFAULT 0,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified_at     TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_order_status
        CHECK (status IN ('pending', 'confirmed', 'cancelled'))
);

CREATE TABLE IF NOT EXISTS content.ticket (
    id                  UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id            UUID        NOT NULL,
    ticket_type_id      UUID        NOT NULL,
    participant_name    VARCHAR(255),
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified_at         TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_ticket_order
        FOREIGN KEY (order_id) REFERENCES content.order(id) ON DELETE RESTRICT,

    CONSTRAINT fk_ticket_ticket_type
        FOREIGN KEY (ticket_type_id) REFERENCES content.ticket_type(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_event_starts_at   ON content.event(starts_at);
CREATE INDEX IF NOT EXISTS idx_event_title       ON content.event USING gin(to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_ticket_type_event ON content.ticket_type(event_id);
CREATE INDEX IF NOT EXISTS idx_ticket_order      ON content.ticket(order_id);