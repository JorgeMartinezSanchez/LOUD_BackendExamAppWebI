-- ============================================
-- SCHEMA
-- ============================================
CREATE SCHEMA IF NOT EXISTS content;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS content.venue (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(255) NOT NULL,
    city        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.event (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id        UUID        NOT NULL,
    title           VARCHAR(80) NOT NULL,
    hour_change     TIMESTAMP WITH TIME ZONE,
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
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
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
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
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
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
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

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_event_starts_at   ON content.event(starts_at);
CREATE INDEX IF NOT EXISTS idx_event_title       ON content.event USING gin(to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_ticket_type_event ON content.ticket_type(event_id);
CREATE INDEX IF NOT EXISTS idx_ticket_order      ON content.ticket(order_id);

-- ============================================
-- SEED DATA (con verificación de existencia)
-- ============================================

-- Venues
INSERT INTO content.venue (id, name, city)
SELECT gen_random_uuid(), 'Estadium Municipal', 'La Paz'
WHERE NOT EXISTS (SELECT 1 FROM content.venue WHERE name = 'Estadium Municipal' AND city = 'La Paz');

INSERT INTO content.venue (id, name, city)
SELECT gen_random_uuid(), 'Centro de Convenciones', 'Santa Cruz'
WHERE NOT EXISTS (SELECT 1 FROM content.venue WHERE name = 'Centro de Convenciones' AND city = 'Santa Cruz');

INSERT INTO content.venue (id, name, city)
SELECT gen_random_uuid(), 'Teatro al Aire Libre', 'Cochabamba'
WHERE NOT EXISTS (SELECT 1 FROM content.venue WHERE name = 'Teatro al Aire Libre' AND city = 'Cochabamba');

INSERT INTO content.venue (id, name, city)
SELECT gen_random_uuid(), 'Sala de Conciertos Rock', 'La Paz'
WHERE NOT EXISTS (SELECT 1 FROM content.venue WHERE name = 'Sala de Conciertos Rock' AND city = 'La Paz');

INSERT INTO content.venue (id, name, city)
SELECT gen_random_uuid(), 'Foro Cultural', 'Sucre'
WHERE NOT EXISTS (SELECT 1 FROM content.venue WHERE name = 'Foro Cultural' AND city = 'Sucre');

-- Events
INSERT INTO content.event (id, venue_id, title, starts_at, description, min_price, total_capacity, available)
SELECT gen_random_uuid(), v.id, 'Rock sin fronteras', NOW() + INTERVAL '7 days', 'La mejor banda de rock nacional', 45.00, 500, 320
FROM content.venue v WHERE v.name = 'Estadium Municipal' AND v.city = 'La Paz'
AND NOT EXISTS (SELECT 1 FROM content.event WHERE title = 'Rock sin fronteras');

INSERT INTO content.event (id, venue_id, title, starts_at, description, min_price, total_capacity, available)
SELECT gen_random_uuid(), v.id, 'Electrónica Fest', NOW() + INTERVAL '14 days', 'DJs internacionales', 60.00, 800, 600
FROM content.venue v WHERE v.name = 'Centro de Convenciones' AND v.city = 'Santa Cruz'
AND NOT EXISTS (SELECT 1 FROM content.event WHERE title = 'Electrónica Fest');

INSERT INTO content.event (id, venue_id, title, starts_at, description, min_price, total_capacity, available)
SELECT gen_random_uuid(), v.id, 'Jazz & Blues Night', NOW() + INTERVAL '21 days', 'Noche de jazz con artistas locales', 35.00, 300, 180
FROM content.venue v WHERE v.name = 'Teatro al Aire Libre' AND v.city = 'Cochabamba'
AND NOT EXISTS (SELECT 1 FROM content.event WHERE title = 'Jazz & Blues Night');

INSERT INTO content.event (id, venue_id, title, starts_at, description, min_price, total_capacity, available)
SELECT gen_random_uuid(), v.id, 'Metal Fest 2026', NOW() + INTERVAL '30 days', 'Las bandas más pesadas del país', 55.00, 400, 150
FROM content.venue v WHERE v.name = 'Sala de Conciertos Rock' AND v.city = 'La Paz'
AND NOT EXISTS (SELECT 1 FROM content.event WHERE title = 'Metal Fest 2026');

INSERT INTO content.event (id, venue_id, title, starts_at, description, min_price, total_capacity, available)
SELECT gen_random_uuid(), v.id, 'Folklore en Vivo', NOW() + INTERVAL '45 days', 'Música tradicional boliviana', 25.00, 250, 200
FROM content.venue v WHERE v.name = 'Foro Cultural' AND v.city = 'Sucre'
AND NOT EXISTS (SELECT 1 FROM content.event WHERE title = 'Folklore en Vivo');

INSERT INTO content.event (id, venue_id, title, starts_at, description, min_price, total_capacity, available)
SELECT gen_random_uuid(), v.id, 'Sinfonía Nocturna', NOW() + INTERVAL '10 days', 'Orquesta sinfónica en concierto', 70.00, 600, 400
FROM content.venue v WHERE v.name = 'Estadium Municipal' AND v.city = 'La Paz'
AND NOT EXISTS (SELECT 1 FROM content.event WHERE title = 'Sinfonía Nocturna');

INSERT INTO content.event (id, venue_id, title, starts_at, description, min_price, total_capacity, available)
SELECT gen_random_uuid(), v.id, 'Reggae Vibes', NOW() + INTERVAL '18 days', 'Noche de reggae con bandas invitadas', 40.00, 450, 300
FROM content.venue v WHERE v.name = 'Centro de Convenciones' AND v.city = 'Santa Cruz'
AND NOT EXISTS (SELECT 1 FROM content.event WHERE title = 'Reggae Vibes');

-- Ticket Types for "Rock sin fronteras"
INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'General', 45.00, 300, 200
FROM content.event e WHERE e.title = 'Rock sin fronteras'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'General');

INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'VIP', 80.00, 100, 60
FROM content.event e WHERE e.title = 'Rock sin fronteras'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'VIP');

INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'Early Bird', 35.00, 100, 60
FROM content.event e WHERE e.title = 'Rock sin fronteras'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'Early Bird');

-- Ticket Types for "Electrónica Fest"
INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'General', 60.00, 500, 400
FROM content.event e WHERE e.title = 'Electrónica Fest'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'General');

INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'VIP', 120.00, 150, 100
FROM content.event e WHERE e.title = 'Electrónica Fest'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'VIP');

INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'Early Bird', 50.00, 150, 100
FROM content.event e WHERE e.title = 'Electrónica Fest'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'Early Bird');

-- Ticket Types for "Jazz & Blues Night"
INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'General', 35.00, 200, 120
FROM content.event e WHERE e.title = 'Jazz & Blues Night'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'General');

INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'VIP', 65.00, 50, 30
FROM content.event e WHERE e.title = 'Jazz & Blues Night'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'VIP');

INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'Early Bird', 25.00, 50, 30
FROM content.event e WHERE e.title = 'Jazz & Blues Night'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'Early Bird');

-- Ticket Types for "Metal Fest 2026"
INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'General', 55.00, 250, 100
FROM content.event e WHERE e.title = 'Metal Fest 2026'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'General');

INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'VIP', 100.00, 100, 30
FROM content.event e WHERE e.title = 'Metal Fest 2026'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'VIP');

INSERT INTO content.ticket_type (id, event_id, name, price, total_capacity, available)
SELECT gen_random_uuid(), e.id, 'Early Bird', 45.00, 50, 20
FROM content.event e WHERE e.title = 'Metal Fest 2026'
AND NOT EXISTS (SELECT 1 FROM content.ticket_type tt WHERE tt.event_id = e.id AND tt.name = 'Early Bird');