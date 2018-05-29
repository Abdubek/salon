$(document).ready(function(){
    if ($('.m-datatable').length) {
        var datatable = $('.m-datatable').mDatatable({
            layout: {
                theme: "default",
                class: "",
                scroll: !1,
                height: null,
                footer: !1
            },
            search: {
                input: $('#generalSearch'),
            }
        });

        $('#m_form_status').on('change', function() {
            //datatable.search($(this).val().toLowerCase(), 'Status');
        });

        $('#m_form_type').on('change', function() {
            //datatable.search($(this).val().toLowerCase(), 'Type');
        });

        $('#m_form_status, #m_form_type').selectpicker();
    }

    $('.is-ajax').submit(function(e){
        e.preventDefault();

        var data = $(this).serialize();
        var url = $(this).attr('action');
        var method = $(this).attr('method');
        var btn = $('button[type="submit"]', this)

        $(btn).toggleClass('m-loader m-loader--light m-loader--right');

        $.ajax({
            url: url,
            method: method,
            data: data,
            success: function(data){
                $(btn).toggleClass('m-loader m-loader--light m-loader--right');
                iziToast.success({
                    title: 'OK',
                    message: data.message,
                });

                if (data.online) {
                    window.location = data.link
                }
                window.location.reload();
            },
            error: function(error){
                $(btn).toggleClass('m-loader m-loader--light m-loader--right');
                console.log(error);
                iziToast.error({
                    title: 'Error',
                    message: error.responseJSON.statusText || error.statusText
                });
                
            }
        })
    });

    $('input[name="phone_number"], input[name="phone"], input[name="client_phone"], input[name="contact"]').inputmask({"mask": "+7 (999) 999-99-99"});
    $("#id_date_of_employment").datepicker({format: 'yyyy-mm-dd'});

    if ($('#m_timetable').length) {
        $('#m_timetable').fullCalendar({
            defaultView: 'listWeek',
            slotMinutes: '00:10:00',
            slotDuration: '00:10:00',
            minTime: '09:00',
            maxTime: '20:00',
            header: {
                left: "prev,next today",
                center: "title",
                right: "month,agendaWeek,agendaDay,listWeek"
            },
            editable: false,
            eventLimit: !0,
            navLinks: !0,
            events: function(start, end, timezone, callback) {
                const lang = window.location.pathname.split('/')[1]

                $.ajax({
                    url: `/${lang}/timetable`,
                    data: {
                        start: start.unix(),
                        end: end.unix()
                    },
                    success: function(data) {
                        var events = [];
                        data.timetables.forEach(function(e) {
                            events.push({
                                id: e.id,
                                title: e.title,
                                description: e.description,
                                start: moment(e.start),
                                end: moment(e.end)
                            });
                        });
                        callback(events);
                    }
                });
            },
            eventRender: function(e, t) {
                t.hasClass("fc-day-grid-event") ? (t.data("content", e.description), t.data("placement", "top"), mApp.initPopover(t)) : t.hasClass("fc-time-grid-event") ? t.find(".fc-title").append('<div class="fc-description">' + e.description + "</div>") : 0 !== t.find(".fc-list-item-title").lenght && t.find(".fc-list-item-title").append('<div class="fc-description">' + e.description + "</div>")
            },
            eventClick: function(calEvent, jsEvent, view) {
                swal(calEvent.title, calEvent.description, "info")
            }
        });
    }

    $('a.dropdown-item.client').click(function(e) {
        e.preventDefault();

        const id = Number($(this).data('id'));
        const name = $(this).data('name');
        const phone = $(this).data('phone');
        const email = $(this).data('email');

        if (id === 0) {
            $('input[name="client_name"]').val('').removeAttr('readonly').removeAttr('disabled');
            $('input[name="client_email"]').val(email).removeAttr('readonly').removeAttr('disabled');
            $('input[name="client_phone"]').val(phone).removeAttr('readonly').removeAttr('disabled');
            $('input[name="client_id"]').val(id);
        } else {
            $('input[name="client_name"]').val(name).attr('readonly', 'true').attr('disabled', 'true');
            $('input[name="client_email"]').val(email).attr('readonly', 'true').attr('disabled', 'true');
            $('input[name="client_phone"]').val(phone).attr('readonly', 'true').attr('disabled', 'true');
            $('input[name="client_id"]').val(id);
        }

    });

    $('a.language-item').click(function(e){
        e.preventDefault();
        $('#set_language_form input[name="language"]').val($(this).data('lang'));
        $('#set_language_form').submit();
    });

    $('#service_duration').timepicker({showMeridian : false, defaultTime: '00:15 AM'});
    $('.category-update').click(function(e){
        e.preventDefault();

        const cid = $(this).data('id');
        const title_kz = $(this).data('title-kz');
        const title_ru = $(this).data('title-ru');
        const gender = $(this).data('gender');
        const lang = window.location.pathname.split('/')[1]

        $('input[name="title_kz"]').val(title_kz);
        $('input[name="title_ru"]').val(title_ru);
        $(`select[name="gender"] option[value="${gender}"]`).attr('selected', '');

        $('#new-category-form').attr('action', `/${lang}/services/category/update/${cid}`);
        $('#category_modal').modal('show');

    });

    $('.delete-obj').click(function(e){
        e.preventDefault();

        const url = $(this).attr('href');
        const title = $(this).data('title');
        const text = $(this).data('text');

        swal({
            title: title,
            text: text,
            type: 'warning',
            showCancelButton: true
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: url,
                    success: function(data){
                        window.location.reload();
                    },
                    error: function(error){
                        console.log(error);
                        iziToast.error({
                            title: 'Error',
                            message: error.statusText
                        });
                    }
                })
            }
        });
    });

    $('#new_session_form #staffer_id').change(function(e){
        e.preventDefault();

        const staffer_id = $('option:selected', this).val();
        const salon_id = $('input[name="salon"]').val();
        const lang = window.location.pathname.split('/')[1]
        const url = `/${lang}/services/salon/${salon_id}`;

        $.ajax({
            url: url,
            data: {m_id: staffer_id},
            success: function(data){
                const tmpl = `${data.categories.map(category => `
                    <optgroup label="${category.name}">
                        ${category.services.map(service => `
                            <option value="${service.id}">${service.name} (${service.price}тг/${service.duration}мин)</option>
                        `)}
                    </optgroup>
                `)}`

                $('#new_session_form #master_services_id').html(tmpl).selectpicker('refresh');
                $('#new_session_form #master_services_id').change();
            },
            error: function(error){
                console.log(error);
                iziToast.error({
                    title: 'Error',
                    message: error.statusText
                });
            }
        });

    });

    $('#new_session_form #master_services_id').change(function(e){
        e.preventDefault();

        const service_id = $('option:selected', this).val();
        const salon_id = $('input[name="salon"]').val();
        const staffer_id = $('#new_session_form #staffer_id option:selected').val();
        const lang = window.location.pathname.split('/')[1]
        const url = `/${lang}/timetable/list/${salon_id}`;

        $.ajax({
            url: url,
            data: {m_id: staffer_id, s_id: service_id},
            success: function(data){
                console.log(data);
                $('#service_start_datetime').datetimepicker({
                    minuteStep: 15,
                    language: data.locale,
                    todayHighlight: true,
                    startDate: moment(data.startDate),
                    weekStart: 1
                });
            },
            error: function(error){
                console.log(error);
                iziToast.error({
                    title: 'Error',
                    message: error.statusText
                });
            }
        });

    });

    $('select').selectpicker('refresh');

    if ($('#new_session_form #staffer_id').length) {
        $('#new_session_form #staffer_id').change();
    }
    
});