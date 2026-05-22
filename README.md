# LOUD_BackendExamAppWebI
Segundo examen parcial de aplicaciones web I con backend

Intentos en el examen del billetito:

    
    def price_update(self, event: Event) :
        if (event.hour_change >= datetime.UTC.):
            query = self.db.query(Event).
  
idea incompleta de crear un endpoint nuevo de price-history pensaba en implementar un metodo en el servicio de events que me permita cambiar el precio y crear otro metodo para avisar que la hora se ha vencido con el datetime de python con datetime.UTCNOW, pero por alguna razón pyhton no detecta que datetime.utcnow() y piensa que no existe pese que esta en la documentacion y que estoy en pyhton 3.13 (la imagen que mi docker ha instalado), tal vez revise mal la documentacion

y sobre la devolucion de current_price y current_tier_id, asumi que Deepseek ya me lo habia hecho... XD

    def get_event_detail(self, event_id: UUID):
        cache_key = f"events:detail:{event_id}"
        
        # Intentar obtener del caché
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Si no está en caché, consultar DB
        event = self.db.query(Event).options(
            joinedload(Event.venue)
        ).filter(Event.id == event_id).first()
        
        if not event:
            return None
        
        ticket_types = self.db.query(TicketType).filter(TicketType.event_id == event_id).all()
        
        result = {
            'id': str(event.id),
            'title': event.title,
            'hour_change': event.hour_change,
            'starts_at': event.starts_at.isoformat() if event.starts_at else None, # type: ignore
            'description': event.description,
            'min_price': float(event.min_price) if event.min_price else None, # type: ignore
            'total_capacity': event.total_capacity,
            'available': event.available,
            'venue': {
                'id': str(event.venue.id),
                'name': event.venue.name,
                'city': event.venue.city
            } if event.venue else None,
            'tiers': [self._serialize_ticket_type(tt) for tt in ticket_types]
        }
        
        # Guardar en caché (TTL 60 segundos)
        cache.set(cache_key, result, ttl=60)
        
        return result

Porque en los metodos get_event_detail de mi event_service.py devolvia todo eso, o puede que quizas este equivocado... he hecho este examen desmotivado, con mucho odio hacia mi mismo... bueno, al menos yo creo que el docker funciona.
