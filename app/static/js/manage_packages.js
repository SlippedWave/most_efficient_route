$(document).ready(function () {
    // Initialize DataTable
    $('#manage_packages_table').DataTable({
        language: {
            url: "//cdn.datatables.net/plug-ins/1.11.3/i18n/es_es.json"
        }
    });

    var initializePackageFormComponents = function () {
        let userTable = $('#select_driver_table').DataTable({
            select: {
                style: 'single'
            },
        });

        let addressTable = $('#select_address_table').DataTable({
            select: {
                style: 'single'
            },
            drawCallback: function (settings) {
                let api = this.api();
                if (api.rows({ filter: 'applied' }).data().length === 0) {
                    $('#select_address_table tbody').html(`
                        <tr>
                            <td colspan="9" class="text-center">
                                No se encontraron registros.
                                <button id="add_new_address_btn" class="btn btn-primary mt-3">Agregar nuevo paquete</button>
                            </td>
                        </tr>
                    `);
                }
            }
        });

        userTable.off('select');
        addressTable.off('select');
        userTable.on('select', function (e, dt, type, indexes) {
            let selectedRowData = userTable.row(indexes[0]).data();
            console.log('Selected row data:', selectedRowData);
        });

        addressTable.on('select', function (e, dt, type, indexes) {
            let selectedRowData = addressTable.row(indexes[0]).data();
            console.log('Selected row data:', selectedRowData);
        });

        $('#set_package_info').off('click', '#add_new_address_btn')

        $('#set_package_info').on('click', '#add_new_address_btn', function () {
            let modalBody = $('#addAddressModal').find('.modal-body');
            modalBody.html('')

            $.ajax({
                url: '/registrar_direccion',
                type: 'GET',
                dataType: 'html',
                success: function (response) {
                    modalBody.html(response);

                    var myModal = new bootstrap.Modal(document.getElementById('addAddressModal'));
                    myModal.show();
                },
                error: function () {
                    alert('Error al cargar el formulario de edición');
                }
            });
        });
    }

    $('button#add-package-btn').on('click', function () {
        let modalBody = $('#addPackageModal').find('.modal-body');
        modalBody.html('');

        $.ajax({
            url: '/registrar_paquete',
            type: 'GET',
            dataType: 'html',
            success: function (response) {
                modalBody.html(response);
                var myModal = new bootstrap.Modal(document.getElementById('addPackageModal'));

                // initializePackageFormComponents();

                myModal.show();
            },
            error: function () {
                alert('Error al cargar el formulario de edición');
            }
        });
    });

    $('body').on('click', '.edit-package-btn', function () {
        let package_id = $(this).data('id');

        let modalBody = $('#editPackageModal').find('.modal-body');
        modalBody.html('');

        $.ajax({
            url: '/editar_paquete/' + package_id,
            type: 'GET',
            dataType: 'html',
            success: function (response) {
                modalBody.html(response);
                var myModal = new bootstrap.Modal(document.getElementById('editPackageModal'));

                initializePackageFormComponents();
                myModal.show();
            },
            error: function () {
                alert('Error al cargar el formulario de edición');
            }
        });
    });



});
